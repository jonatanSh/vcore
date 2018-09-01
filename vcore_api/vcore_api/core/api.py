from ..assets.docker.docker_asset_collector import DockerAssetCollector
from ..assets.base.io import IoAsset
from .reqeust_handler import RequestHandler


class Api(object):
    def __init__(self, host="http://localhost", port=5002):
        self.host = host
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
