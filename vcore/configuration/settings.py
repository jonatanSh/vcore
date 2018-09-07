import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE = {
    "connection_string": "sqlite:///database.db",
}

API = {
    "host": "0.0.0.0",
    "port": 5002,
    "debug": True,
    "upload_folder": os.path.join(BASE_DIR, "uploads"),
}

LOGGING = {
    "level": logging.DEBUG,
}

CELERY = {
    "broker": "amqp://172.16.224.129//",
    "backend": "db+sqlite:///{0}".format(os.path.join(BASE_DIR, "celery.db")),
    "loglevel": "info",
    "engine_name": "celery_async_engine",
    "provider_timeout": 0.05  # seconds
}

ENABLED_SERVICES = [
    "docker",
]

BACKENDS = {
    "storage": "vcore.api.backends.storage.disk",
}

DISK_API_SETTINGS = {
    "directory": API["upload_folder"],
}

DOCKER = {
    "client_url": "tcp://172.16.224.128:2375"  # "unix://var/run/docker.sock"
}
