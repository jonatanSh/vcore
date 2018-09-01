from vcore.tasks.api.task_objects import Task
from vcore.api.plugins.utils import api_base_wrapper
from vcore.services.docker.query_service.images import QueryObject, Queries


class QueryImagesList(Task):
    def task_handle_get(self, *args, **kwargs):
        return api_base_wrapper(QueryObject(Queries.LIST_IMAGES).handle(*args, **kwargs))
