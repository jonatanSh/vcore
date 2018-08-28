import logging
import os
import sys
from flask import Flask
from flask_restful import Api
from vcore.tasks.api.integration import make_celery
# must import task importer for shared settings.
from vcore.tasks.tasks_importer import *

logger = logging.getLogger(__file__)

from vcore.configuration.conf_loader import Settings


def setup(app):
    Settings.flask_app = app
    Settings.api = Api(Settings.runtime.flask_app)
    Settings.celery = make_celery(Settings.runtime.flask_app)  # sets up celery

    Settings.routes = []

    for service_name, service_settings in Settings.plugins.items():
        base_uri = "/" + service_name + "/{0}"
        for plugin_path, plugin_settings in service_settings.PLUGINS.items():
            sys_path = os.path.join(Settings.settings.BASE_DIR, os.path.dirname(plugin_path))
            import_name = os.path.basename(plugin_path).replace(".py", "")
            sys.path.append(sys_path)

            try:
                module = __import__(import_name)
            except Exception as error:
                logging.error("Plugin import error: {0} in {1}, import_name = {2}".format(error, sys_path, import_name))
                sys.path.remove(sys_path)
                continue

            try:
                handler = getattr(module, plugin_settings.handler)
            except Exception as error:
                logging.error("Plugin handler not found error: {0}".format(error))
                sys.path.remove(sys_path)
                continue

            for route in plugin_settings.routes:
                current_route = base_uri.format(route)
                Settings.runtime.routes.append(current_route)
                Settings.runtime.api.add_resource(handler, current_route)


def run(app):
    with app.app_context():
        setup(app)
    logging.info("Routes:\n{0}".format("\n".join(Settings.runtime.routes)))
    Settings.runtime.flask_app.run(port=Settings.settings.API.port, debug=Settings.settings.API.debug)
