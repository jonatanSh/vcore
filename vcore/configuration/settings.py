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
    "backend": "db+sqlite:///{0}".format(os.path.join(BASE_DIR, "celery.db")),
    "loglevel": "info",
    "engine_name": "celery_async_engine",
    "provider_timeout": 0.05  # seconds
}

ENABLED_SERVICES = [
    "docker",
]
