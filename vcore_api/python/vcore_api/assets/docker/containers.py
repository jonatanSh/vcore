from ..base_asset import Asset
from ...collections import PortsCollection
from ...core.response import JsonResponse
from ...core.exceptions import GeneralApiError, IncompatibleObject


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

    def run(self, image, detach, ports=None, command=None, name=None):
        if not ports:
            ports = PortsCollection.create_collection()
        if not isinstance(ports, PortsCollection):
            raise IncompatibleObject("argument image must be asset of collections.PortsCollection")
        kwargs = {
            "image": image,
            "command": command,
            "detach": detach,
            "ports": ports.to_str(),
            "name": name
        }

        return self.requests.post("docker/run", ResponseObject=JsonResponse, parameters=kwargs)

    def status(self, container):
        return self.requests.get("docker/query/containers/info/{0}".format(container), ResponseObject=JsonResponse)
