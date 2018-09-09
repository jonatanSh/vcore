from ..base_asset import Asset
from .images import Image
from .networks import Networks
from .containers import Containers


class DockerAssetCollector(Asset):

    @property
    def images(self):
        return Image(self.requests, self.api)

    @property
    def containers(self):
        return Containers(self.requests, self.api)

    @property
    def networks(self):
        return Networks(self.requests, self.api)
