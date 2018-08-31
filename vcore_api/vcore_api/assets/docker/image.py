from ..base_asset import Asset
from ...core.response import JsonResponse


class Image(Asset):

    def build(self):
        return self.requests.get("docker/build", ResponseObject=JsonResponse)

    def __str__(self):
        return "ImageAsset(methods: [build])"
