import logging
from . import settings

logging.basicConfig(**settings.LOGGING_SETTINGS)


def get_logger(script_name):
    return logging.getLogger(script_name)
