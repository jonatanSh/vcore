from celery.result import AsyncResult
from vcore.tasks.api.task_objects import Task
from vcore.tasks.api.celery import celery_engine


class Provider(Task):
    def task_handle_get(self, request_id):
        return {"status": AsyncResult(request_id, app=celery_engine).state}
