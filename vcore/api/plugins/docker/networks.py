from flask_restful import reqparse
from vcore.tasks.api.task_objects import Task
from vcore.services.docker.networks.networks import NetWorkManager


class CreateNetwork(Task):
    def task_handle_post(self, *args, **kwargs):
        parse = reqparse.RequestParser()
        arguments = list(NetWorkManager.create.__code__.co_varnames)
        for argument in arguments:
            parse.add_argument(argument)

        options = parse.parse_args()

        return NetWorkManager.create(**options)
