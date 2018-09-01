from ..base_asset import Asset
from ...core.response import JsonResponse
from ...core.exceptions import GeneralApiError


class Image(Asset):
    def build(self, local_path):
        response = self.api.io.upload(local_path)
        return self.requests.get("docker/build/{0}".format(response.file_id), ResponseObject=JsonResponse)

    def list(self):
        response = self.requests.get("docker/query/images/list", ResponseObject=JsonResponse)
        if "images" in response:
            return response.images
        else:
            return GeneralApiError(response, "Error key images not found")
