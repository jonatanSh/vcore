import pika
import pymongo
from contextlib import contextmanager
import gridfs
import socket
import json
import logging

from .utils import settings
from .networking.packet import PacketCreationActions, Packet

logging.getLogger("pika").propagate = False

logging.basicConfig(filename='/var/log/lib.logs', level=logging.DEBUG)
logger = logging.getLogger(__file__)


# TODO refactor
class Docker(object):
    def __init__(self):
        self.host = socket.socket()
        logging.info("connecting to docker host")
        self.connected = False

    def check_connection(self):
        if not self.connected:
            self.host.connect((settings.DOCKER_HOST["host"], settings.DOCKER_HOST["port"]))  # hard coded remove later
            self.connected = True

    def mk_request(self, action, **kwargs):
        self.check_connection()
        request = {"action": action}
        request.update({"kwargs": kwargs})
        packet = Packet(request, PacketCreationActions.ENCODE)
        return packet.send_and_receive(self.host)

    def build(self, path, name, cache=True):
        return self.mk_request(action="build", path=path, name=name, cache=cache)

    def run_challenge(self, name, port):
        return self.mk_request(action="run", name=name, port=port).data


@contextmanager
def mongo_connection():
    connection = pymongo.MongoClient(**settings.MONGO)
    try:
        yield connection
    except Exception as e:
        connection.close()
        raise e


@contextmanager
def mongo_fs(db, collection):
    with mongo_connection() as mongo:
        yield gridfs.GridFS(database=mongo[db], collection=collection)


@contextmanager
def rabbit_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBIT))

    try:
        yield connection.channel()
    except Exception as e:
        connection.close()
        raise e


class Rabbit(object):
    queues_declares = []

    def send(self, data, queue, force=False, queue_args=None):
        with rabbit_connection() as server:
            if not force:
                self.declare_queue(name=queue, queue_args=queue_args)
            server.basic_publish(routing_key=queue, body=json.dumps(data), exchange="")

    def declare_queue(self, name, connection=None, queue_args=None):
        if queue_args is None:
            queue_args = {}
        if name not in self.queues_declares:
            self.queues_declares.append(name)
            if not connection:
                with rabbit_connection() as mq_connection:
                    mq_connection.queue_declare(queue=name, durable=True, arguments=queue_args)
            else:
                connection.queue_declare(queue=name, durable=True, arguments=queue_args)

    def setup(self, queues):
        for queue in queues:
            self.declare_queue(queue['queue'], queue_args=queue['args'])


rabbit = Rabbit()
