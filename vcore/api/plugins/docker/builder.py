from flask_restful import reqparse
from vcore.tasks.api.task_objects import Task
from vcore.services.docker.builder.builder import build_image
from vcore.api.plugins.utils import async_request


class Builder(Task):
    def task_handle_post(self, *args, **kwargs):
        parse = reqparse.RequestParser()
        parse.add_argument('file_id')
        parse.add_argument("tag")
        options = parse.parse_args()
        return async_request(build_image.apply_async(args, options, queue="task_builder"))
