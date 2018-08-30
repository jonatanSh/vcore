from vcore.tasks.api.celery import celery_engine


@celery_engine.task(name="Builder.handle", trail=True)
def handle(*args, **kwargs):
    return "Builder->handle"
