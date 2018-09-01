import json
import inspect


class Asset(object):
    def __init__(self, requests, api):
        self.requests = requests
        self.api = api

    def __str__(self, deep=True):
        if not deep:
            return super(Asset, self).__str__()
        members = {}
        for method_tuple in inspect.getmembers(object=self):
            if not method_tuple[0].startswith("_") and method_tuple[0] not in [
                "api",
                "requests"
            ]:
                try:
                    members[method_tuple[0]] = method_tuple[1].__str__(deep=False)
                except:
                    members[method_tuple[0]] = str(method_tuple[1])

        return json.dumps({
            "Asset": self.__class__.__name__,
            "Members": members,
        }, indent=2)

    def __repr__(self):
        return "{0}({1}, to print the object is str(object))".format(self.__class__.__name__,
                                                                     super(Asset, self).__repr__())
