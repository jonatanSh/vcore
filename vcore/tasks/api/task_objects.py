from flask_restful import Resource


class Task(Resource):
    def task_handle_get(self, *args, **kwargs):
        pass

    def task_handle_post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        return self.task_handle_get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.task_handle_post(*args, **kwargs)
