import socket
import os
import select
from queue import Queue, Empty
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from environment.utils.logger import get_logger
from environment.networking.packet import Packet, PacketCreationActions
from environment.utils import settings

logger = get_logger(__file__)


class Server(object):
    def __init__(self, handler):
        self.server_socket = socket.socket()
        self.clients = {}
        self.rlist = [self.server_socket]
        self.wlist = []
        self.elist = []
        self.handler = handler

    def start(self):
        connection_tuple = (settings.DOCKER_HOST["server_host"], settings.DOCKER_HOST["port"])
        logger.info("starting server on {0}".format(connection_tuple))
        self.server_socket.bind(connection_tuple)
        self.server_socket.listen(settings.DOCKER_HOST["backlog"])

    def handle(self):
        rlist, wlist, elist = select.select(self.rlist, self.wlist, self.elist)

        for sock in rlist:
            if sock == self.server_socket:
                client, address = self.server_socket.accept()
                logger.info("Accepted new connection from: {0}".format(address))
                self.clients[client] = Queue()
                self.rlist.append(client)

            else:
                data = sock.recv(1024)
                if data:
                    logger.info("Handling data from {0}".format(sock))
                    self.clients[sock].put(self.handler(Packet(data, PacketCreationActions.DECODE)))
                    if sock not in self.wlist:
                        self.wlist.append(sock)
                else:
                    logger.info("Disconnected {0}".format(sock))
                    if sock in self.rlist:
                        self.rlist.remove(sock)
                    if sock in self.wlist:
                        self.wlist.remove(sock)
                    sock.close()
                    del self.clients[sock]

        for sock in wlist:
            if sock not in self.clients:
                continue
            try:
                next_message = self.clients[sock].get_nowait()
            except Empty:
                pass
            else:
                logger.info("Sending data to {0}".format(sock))
                packet = Packet(next_message, PacketCreationActions.ENCODE)
                packet.send_packet(sock)

        for sock in elist:
            logger.info("Disconnected {0}".format(sock))
            if sock in self.rlist:
                self.rlist.remove(sock)
            if sock in self.wlist:
                self.wlist.remove(sock)
            sock.close()
            del self.clients[sock]
