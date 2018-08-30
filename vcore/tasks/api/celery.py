from celery import Celery
from vcore.configuration.conf_loader import Settings


def create_engine():
    celery = Celery(Settings.settings.CELERY.engine_name, backend=Settings.settings.CELERY.backend,
                    broker=Settings.settings.CELERY.broker)

    Settings.celery_engine = celery


if "celery_engine" not in Settings.runtime:
    create_engine()

celery_engine = Settings.runtime.celery_engine
