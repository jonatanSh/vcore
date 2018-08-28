import json
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from environment.utils.logger import get_logger

logger = get_logger(__file__)


class BasePacket(object):
    def __init__(self):
        self.packet = None

    def is_valid(self):
        return self.packet is not None

    def send_packet(self, sock):
        sock.send(self.packet)

    def send_and_receive(self, sock):
        self.send_packet(sock)
        return Packet(sock.recv(2 ** 32), PacketCreationActions.DECODE)


class RequestPacket(BasePacket):
    def __init__(self, packet):
        super(RequestPacket, self).__init__()
        self.log = ""
        try:
            self.packet = json.loads(packet.decode("utf-8"))
        except Exception as error:
            self.packet = None
            logger.error("Invalid packet: \n{0}\nerror:\n{1}".format(packet, error))

    @property
    def action(self):
        return self.packet["action"]

    @property
    def args(self):
        return self.packet.get("args", [])

    @property
    def kwargs(self):
        return self.packet.get("kwargs", {})

    @property
    def data(self):
        return self.packet.get("data", {})


class ResponsePacket(BasePacket):
    def __init__(self, packet):
        super(ResponsePacket, self).__init__()
        self.packet = json.dumps(packet).encode("utf-8")


class PacketCreationActions(object):
    DECODE = "decode"
    ENCODE = "encode"


# packet factory
def Packet(packet, action="Unknown"):
    if type(packet) is bytes or action == PacketCreationActions.DECODE:
        return RequestPacket(packet)

    return ResponsePacket(packet)
