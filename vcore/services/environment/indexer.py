import sys
import django
import pika
import json
import os

DIR_NAME = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(DIR_NAME, "challenge_framework"))

sys.path.append(DIR_NAME)

from environment.lib import rabbit
from environment.utils import settings
from environment.utils.logger import get_logger

logger = get_logger(__file__)

os.environ["DJANGO_SETTINGS_MODULE"] = "challenge_framework.settings"

django.setup()

from challenge_processor.models import Challenge


# can use models now


class Indexer(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBIT))
        self.channel = self.connection.channel()
        self.queue = settings.CHALLENGES['ready_challenges_queue']
        rabbit.setup(
            [
                {
                    "queue": self.queue,
                    "args": {},
                }
            ]
        )

    def consume(self):
        logger.info("Indexer start consuming listening on {} ... ".format(self.queue))
        while True:
            message = self.channel.basic_get(queue=self.queue)
            self.process(*message)
            self.connection.sleep(1)

    def process(self, method, properties, body):
        if method and properties and body:
            body = json.loads(body.decode('utf-8'))
            cid = body['challenge_id']
            logger.info("indexing {0}".format(cid))

            try:
                challenge = Challenge.objects.get(cid=cid)
            except Exception as error:
                print("Error => {}".format(error))
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
                return

            challenge.output = body['output']

            challenge.ready = not body["error"]
            challenge.save()

            self.channel.basic_ack(delivery_tag=method.delivery_tag)


indexer = Indexer()
indexer.consume()
