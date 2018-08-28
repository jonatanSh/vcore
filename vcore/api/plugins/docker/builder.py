from vcore.tasks.api.task_objects import Task
from vcore.services.docker.builder.builder import handle


class Builder(Task):
    def task_handle_get(self, *args, **kwargs):
        handle(*args, *kwargs)
