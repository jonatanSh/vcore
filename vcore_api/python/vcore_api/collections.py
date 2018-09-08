import json


class PortsCollection(object):
    def __init__(self):
        self._ports = {}

    def add_tcp_port(self, src, bind):
        self._ports["{0}/tcp".format(src)] = bind

    def add_udp_port(self, src, bind):
        self._ports["{0}/udp".format(src)] = bind

    @staticmethod
    def create_collection():
        return PortsCollection()

    def to_dict(self):
        return self._ports

    def to_str(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return json.dumps({
            "object": "PortsCollection",
            "ports": self.to_dict()
        }, indent=2)
