from ..base_asset import Asset
from ...core.response import JsonResponse
from ...core.exceptions import GeneralApiError


class Containers(Asset):
    def list(self, all=False):
        append = "/alive"
        if all:
            append = ""
        response = self.requests.get("docker/query/containers/list{}".format(append), ResponseObject=JsonResponse)
        if "containers" in response:
            return response.containers
        else:
            return GeneralApiError(response, "Error key containers not found")
