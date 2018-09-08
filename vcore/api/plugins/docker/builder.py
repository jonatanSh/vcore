from vcore.tasks.api.task_objects import Task
from vcore.services.docker.builder.builder import build_image
from vcore.api.plugins.utils import async_request


class Builder(Task):
    def task_handle_post(self, *args, **kwargs):
        return async_request(build_image.apply_async(args, kwargs, queue="task_builder"))
