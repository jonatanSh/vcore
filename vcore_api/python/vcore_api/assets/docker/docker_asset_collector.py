from ..base_asset import Asset
from .images import Image
from .containers import Containers


class DockerAssetCollector(Asset):

    @property
    def images(self):
        return Image(self.requests, self.api)

    @property
    def containers(self):
        return Containers(self.requests, self.api)
