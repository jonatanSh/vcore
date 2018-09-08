from ..assets.docker.docker_asset_collector import DockerAssetCollector
from ..base.io import IoAsset
from .reqeust_handler import RequestHandler
from .response import JsonResponse


class Api(object):
    def __init__(self, host="http://localhost", port=5002):
        self.host = host
        if not host.startswith("http://"):
            host = "http://{0}".format(host)
        self.port = port
        self._requests = RequestHandler(host=host, port=port)

    @property
    def docker(self):
        return DockerAssetCollector(self._requests, self)

    @property
    def io(self):
        return IoAsset(self._requests, self)

    def __str__(self):
        return "VcoreApi({0}:{1})".format(self.host, self.port)

    def __repr__(self):
        return str(self)

    def get_task(self, request_id):
        done_url = "/api/request/is_done/{0}".format(request_id)
        response = self._requests.get(done_url, ResponseObject=JsonResponse)
        try:  # response object might not support item assignment
            response.response_object["is_done_url"] = done_url
        except:
            pass
        return response
