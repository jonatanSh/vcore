import inspect
from vcore.services.docker.lib.engine import docker_engine


class Queries(object):
    LIST_IMAGES = "list_images"
    LIST_CONTAINERS_ALL = "list_containers_all"
    LIST_CONTAINERS = "list_containers"
    CONTAINER_INFO = "container_info"


class QueryObject(object):
    def __init__(self, specific_query):
        self.queries = [member[1] for member in inspect.getmembers(Queries) if not member[0].startswith("_")]
        self.specific_query = specific_query

    def handle(self, *args, **kwargs):
        if self.specific_query in self.queries:
            if not hasattr(self, self.specific_query):
                return {
                    "Error": True,
                    "Message": "Query error {0}, query doesn't exists".format(self.specific_query),
                    "Avilable queries": self.queries
                }
            else:
                return getattr(self, self.specific_query)(*args, **kwargs)

    @staticmethod
    def list_images():
        images = []
        for image in docker_engine.images.list(all=True):
            images += image.tags
        return {
            "images": images
        }

    @staticmethod
    def list_containers_all():
        containers = []
        for container in docker_engine.containers.list(all=True):
            containers.append(container.name)
        return {
            "containers": containers
        }

    @staticmethod
    def list_containers():
        containers = []
        for container in docker_engine.containers.list():
            containers.append(container.name)
        return {
            "containers": containers
        }

    @staticmethod
    def container_info(container):
        try:
            container = docker_engine.containers.get(container)
            if hasattr(container, "attrs"):
                return container.attrs
        except Exception as error:
            return {
                "container_query_error": str(error)
            }
