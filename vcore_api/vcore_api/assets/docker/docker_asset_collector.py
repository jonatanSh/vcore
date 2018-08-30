from ..base_asset import Asset
from .image import Image


class DockerAssetCollector(Asset):

    @property
    def image(self):
        return Image(self.requests)

    def __str__(self):
        return "\n".join([
            "DockerAsset sub modules",
            "   -> image"
        ])
