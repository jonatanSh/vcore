import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE = {
    "connection_string": "sqlite:///database.db",
}

API = {
    "port": 5002,
    "debug": True,
}

LOGGING = {
    "level": logging.DEBUG,
}

CELERY = {
    "broker": "amqp://localhost//",
    "backend": "sqlite:///database.db",
    "loglevel": "info",
}

ENABLED_SERVICES = [
    "docker",
]
