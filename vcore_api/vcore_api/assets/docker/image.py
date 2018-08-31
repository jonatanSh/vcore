from ..base_asset import Asset
from ...core.response import JsonResponse


class Image(Asset):
    def build(self, local_path):
        response = self.api.io.upload(local_path)
        return self.requests.get("docker/build/{0}".format(response.file_id), ResponseObject=JsonResponse)

    def __str__(self):
        return "ImageAsset(methods: [build])"
