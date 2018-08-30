from vcore.tasks.api.task_objects import Task


class Provider(Task):
    def task_handle_get(self, request_id):
        return "unknown"
