import inspect
from vcore.services.docker.lib.engine import docker_engine


class Queries(object):
    LIST_IMAGES = "list_images"


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

    def list_images(self):
        images = []
        for image in docker_engine.images.list():
            images += image.tags
        return {
            "images": images
        }
