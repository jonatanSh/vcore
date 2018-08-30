from vcore.tasks.api.task_objects import Task
from vcore.services.docker.builder.builder import handle
from vcore.api.plugins.utils import async_request


class Builder(Task):
    def task_handle_get(self, *args, **kwargs):
        return async_request(handle.delay(*args, *kwargs))
