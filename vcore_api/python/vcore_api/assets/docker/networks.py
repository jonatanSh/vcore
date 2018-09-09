from ..base_asset import Asset
from docker.types import IPAMConfig
from ...core.response import JsonResponse
from ...core.exceptions import IncompatibleObject


class Networks(Asset):
    class SCOPES(object):
        LOCAL = "local"
        GLOBAL = "global"
        SWARM = "swarm"
        _AVILABLE = [
            LOCAL,
            GLOBAL,
            SWARM
        ]

    def create(self, name, driver=None, options=None, ipam=None, check_duplicate=None, internal=None, labels=None,
               enable_ipv6=None, attachable=None, scope=None, ingress=None):
        # for true use boolean for false use None for serialization
        if options is None:
            options = {}

        if ipam and type(ipam) is not IPAMConfig:
            raise IncompatibleObject("ipam config type must be docker.types.IPAMConfig")

        if scope and scope not in Networks.SCOPES._AVILABLE:
            raise IncompatibleObject("network scope must be Networks.SCOPES.<scope>")

        kwargs = {
            "name": name,
            "driver": driver,
            "options": options,
            "ipam": ipam,
            "check_duplicate": check_duplicate,
            "internal": internal,
            "labels": labels,
            "enable_ipv6": enable_ipv6,
            "attachable": attachable,
            "scope": scope,
            "ingress": ingress
        }

        return self.requests.post("/docker/networks/create", parameters=kwargs, ResponseObject=JsonResponse)
