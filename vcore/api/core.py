from flask import Flask
from flask_restful import Api

from vcore.configuration.conf_loader import Settings


def setup():
    Settings.flask_app = Flask(__name__)
    Settings.api = Api(Settings.runtime.flask_app)
    Settings.runtime.api.add_resource(Employees, '/employees')  # Route_1


def run():
    Settings.runtime.api.run(port=Settings.settings.api.port)
