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
    "backend": "db+sqlite:///database.db",
    "loglevel": "info",
    "engine_name": "celery_async_engine",
}

ENABLED_SERVICES = [
    "docker",
]
