import json
import os
from vcore.configuration import settings as _settings  # to not confuse with Settings

BASE_DIR = os.path.dirname(__file__)


class SettingsNotFoundException(Exception):
    def __init__(self, error_message, obj):
        self.error_message = error_message
        if type(obj) is dict:
            try:
                obj = json.dumps(obj, indent=2)
            except Exception:
                pass

        self.obj = obj

    def __str__(self):
        return "SettingsNotFound: {0}, in {1}".format(self.error_message, self.obj)


class ConfigurationObject(object):
    def __init__(self, loaded_configuration):
        self.loaded_configuration = loaded_configuration

    def __getattr__(self, item):
        if type(self.loaded_configuration) is dict:
            try:
                value = self.loaded_configuration[item]
            except (Exception, AttributeError):
                raise SettingsNotFoundException(item, self.loaded_configuration)
        else:
            if hasattr(self.loaded_configuration, item):
                value = getattr(self.loaded_configuration, item)
            else:
                raise SettingsNotFoundException(item, self.loaded_configuration)
        if type(value) is dict:
            return ConfigurationObject(value)
        else:
            return value

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        try:
            conf = json.dumps(
                self.loaded_configuration,
                indent=2
            )
        except Exception:
            conf = self.loaded_configuration
        return "ConfigurationObject({0})".format(conf)

    def __contains__(self, item):
        return item in self.loaded_configuration

    def __iter__(self):
        for item in self.loaded_configuration:
            if type(item) is dict:
                yield ConfigurationObject(item)
            else:
                yield item

    def items(self):
        for key, value in self.loaded_configuration.items():
            if type(value) is dict:
                yield key, ConfigurationObject(value)


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
        return ConfigurationObject(self._runtime)

    def __setattr__(self, key, value):
        PROTECTED_ATTARS = [
            "_runtime",
            "_plugins",
        ]
        if key in PROTECTED_ATTARS:
            return super(LazySettings, self).__setattr__(key, value)

        if key in self._runtime:
            return setattr(self._runtime, key, value)

        self._runtime[key] = value


Settings = LazySettings()
