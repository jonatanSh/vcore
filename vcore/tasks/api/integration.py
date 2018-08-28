from celery import Celery
from vcore.configuration.conf_loader import Settings


def make_celery(app):
    celery = Celery(app.import_name, backend=Settings.settings.CELERY.backend,
                    broker=Settings.settings.CELERY.broker)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.config["celery"] = celery
    return celery
