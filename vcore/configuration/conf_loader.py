import json
import os
from vcore.configuration import settings as _settings  # to not confuse with Settings

BASE_DIR = os.path.dirname(__file__)


class ConfigurationObject(object):
    def __init__(self, loaded_configuration):
        self.loaded_configuration = loaded_configuration

    def __getattr__(self, item):
        value = getattr(self.loaded_configuration, item)
        if type(item) is dict:
            return ConfigurationObject(item)
        else:
            return value

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        return "ConfigurationObject({0})".format(json.dumps(
            self.loaded_configuration,
            indent=2
        ))

    def __contains__(self, item):
        return item in self.loaded_configuration

    def items(self):
        return self.loaded_configuration.items()


class LazySettings(object):
    def __init__(self):
        self._plugins = None
        self._runtime = {}

    def load_plugins(self):
        with open(os.path.join(BASE_DIR, "plugins.json"), "r") as pfile:
            self._plugins = json.load(pfile)

    @property
    def plugins(self):
        if not self._plugins:
            self.load_plugins()
        return ConfigurationObject(self._plugins)

    @property
    def settings(self):
        return ConfigurationObject(_settings)

    @property
    def runtime(self):
        return ConfigurationObject(self.runtime)

    def __setattr__(self, key, value):
        self.runtime[key] = value


Settings = LazySettings()
