import importlib
from vcore.configuration.conf_loader import Settings


class API(object):
    STORAGE = "storage"


def get_backend(api_enum):
    module = importlib.import_module(Settings.settings.BACKENDS[api_enum])

    api = getattr(module, "create_api")()

    return api
