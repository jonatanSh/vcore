from vcore.tasks.api.task_objects import Task
from vcore.api.plugins.utils import api_base_wrapper
from vcore.services.docker.query_service import QueryObject, Queries


class QueryImagesList(Task):
    def task_handle_get(self, *args, **kwargs):
        return api_base_wrapper(QueryObject(Queries.LIST_IMAGES).handle(*args, **kwargs))


class QueryContainersList(Task):
    def task_handle_get(self, *args, **kwargs):
        return api_base_wrapper(QueryObject(Queries.LIST_CONTAINERS_ALL).handle(*args, **kwargs))


class QueryContainersListAlive(Task):
    def task_handle_get(self, *args, **kwargs):
        return api_base_wrapper(QueryObject(Queries.LIST_CONTAINERS).handle(*args, **kwargs))


class QueryContainerInfo(Task):
    def task_handle_get(self, *args, **kwargs):
        return api_base_wrapper(QueryObject(Queries.CONTAINER_INFO).handle(*args, **kwargs))
