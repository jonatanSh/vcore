from ..base_asset import Asset
from .image import Image


class DockerAssetCollector(Asset):

    @property
    def images(self):
        return Image(self.requests, self.api)
