from vcore.tasks.api.task_objects import Task


class Handler(Task):
    def task_handle_get(self):
        return "this task is sync"
