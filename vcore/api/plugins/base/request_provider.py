from celery.result import AsyncResult
from celery.states import SUCCESS, FAILURE
from vcore.tasks.api.task_objects import Task
from vcore.tasks.api.celery import celery_engine
from vcore.api.plugins.utils import api_base_wrapper
from vcore.configuration.conf_loader import Settings


class Provider(Task):
    def task_handle_get(self, request_id):
        task = AsyncResult(request_id, app=celery_engine)
        output = None
        if task.state in [
            SUCCESS,
            FAILURE
        ]:
            output = task.get(timeout=Settings.settings.CELERY.provider_timeout)
        return api_base_wrapper(
            {
                "status": task.state,
                "output": output
            })
