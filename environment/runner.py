import sys
import django
import pika
import json
import os
from random import randint

DIR_NAME = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(DIR_NAME, "challenge_framework"))

sys.path.append(DIR_NAME)

from environment.lib import settings, Docker, rabbit
from environment.utils.logger import get_logger

logger = get_logger(__file__)

os.environ["DJANGO_SETTINGS_MODULE"] = "challenge_framework.settings"

django.setup()

from challenge_runner.models import RunningChallenge, RunningHost


# can use models now

class Runner(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBIT))
        self.channel = self.connection.channel()
        self.queue = settings.CHALLENGES['run_challenge_queue']
        self.client = Docker()
        rabbit.setup(
            [
                {
                    "queue": self.queue,
                    "args": {},
                }
            ]
        )

    def consume(self):
        logger.info("Runner start consuming listening on {} ... ".format(self.queue))
        while True:
            message = self.channel.basic_get(queue=self.queue)
            self.process(*message)
            self.connection.sleep(1)

    def process(self, method, properties, body):
        if method and properties and body:
            body = json.loads(body.decode('utf-8'))
            cid = body['cid']
            logger.info("Running a new challenge {0}".format(cid))
            action = body["action"]
            try:
                challenge = RunningChallenge.get(None, challenge_id=cid)
                if action == "run":
                    self.run(challenge)
            except Exception as error:
                print(error)
                logger.info("Error => {}".format(error))
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
                return

            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self, challenge):
        host = RunningHost.get(host=self.client.host.getsockname()[0])
        ports = host.get_open_ports()
        port = randint(4445, 65535)
        while port in ports:
            port = randint(4445, 65535)

        host.add_port(port)
        logger.info(self.client.run_challenge(name=challenge.challenge.cid, port=port))

        challenge.update_state(save=False)
        challenge.host = host
        challenge.port = port
        challenge.save()


runner = Runner()
runner.consume()
