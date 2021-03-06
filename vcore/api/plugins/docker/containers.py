from flask_restful import reqparse
from vcore.tasks.api.task_objects import Task
from vcore.services.docker.containers.runner import run
from vcore.services.docker.containers.general import exec_command
from vcore.api.plugins.utils import async_request


class Run(Task):
    def task_handle_post(self, *args, **kwargs):
        parse = reqparse.RequestParser()
        parse.add_argument('image')
        parse.add_argument('command')
        parse.add_argument("detach")
        parse.add_argument("ports")
        parse.add_argument("name")
        options = parse.parse_args()
        return async_request(run.apply_async(args, options, queue="task_runner"))


class Execute(Task):
    def task_handle_post(self, *args, **kwargs):
        parse = reqparse.RequestParser()
        parse.add_argument('container')
        parse.add_argument('command')
        options = parse.parse_args()
        return exec_command(**options)
