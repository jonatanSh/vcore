from vcore.tasks.api.task_objects import celery


@celery.task(name="Builder.handle")
def handle(*args, **kwargs):
    return "Builder->handle"


"""
import pika
import json
from bson import ObjectId
import tempfile
import os
import shutil
import logging
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from environment.lib import mongo_fs, settings, Docker, rabbit
from environment.utils.logger import get_logger

logger = get_logger(__file__)


class Builder(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBIT))
        self.channel = self.connection.channel()
        self.queue = settings.CHALLENGES['process_challenges_queue']
        self.collection = settings.CHALLENGES['challenge_collection']
        self.client = Docker()
        self.ready_queue = settings.CHALLENGES['ready_challenges_queue']

        rabbit.setup(
            [
                {
                    "queue": self.queue,
                    "args": {},
                },
                {
                    "queue": self.ready_queue,
                    "args": {},
                }
            ]
        )

    def consume(self):
        print("Builder start consuming listening on {} ... ".format(self.queue))
        while True:
            message = self.channel.basic_get(queue=self.queue)
            self.process(*message)
            self.connection.sleep(1)

    def process(self, method, properties, body):
        if method and properties and body:
            body = json.loads(body.decode('utf-8'))
            cid = body['challenge_id']
            with mongo_fs(db=settings.CHALLENGES['db'], collection=self.collection) as fs:
                object_id = ObjectId(body['object_id'])
                print('processing {} ... '.format(object_id))
                document = fs.find_one({'_id': object_id})
                path = tempfile.mkdtemp(suffix=cid)
                real_path = os.path.join(path, 'challenge.zip')
                with open(real_path, 'wb+') as file:
                    file.write(document.read())

                shutil.unpack_archive(real_path, extract_dir=os.path.join(path, 'challenge'))

            output, error = self.build(os.path.join(path, 'challenge'), cid=cid)
            logger.info("Build output: {0}, error={1}".format(output, error))
            rabbit.send({
                'output': output,
                'challenge_id': cid,
                'error': error

            }, queue=self.ready_queue)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def build_python_environment(manifest, path):
        env = manifest['environment']

        with open(os.path.join(os.path.dirname(path), 'dockerfile'), "w+") as docker_file:
            docker_file.write('\n'.join([
                "FROM jonatansh/challenge_framework:{}".format(env['image']),
                "COPY challenge/requirements.txt /req.txt",
                "COPY challenge /challenge",
                "RUN python -m pip install -r /req.txt",
            ]))

    def build_environment(self, manifest, path):
        builders = {
            'python': self.build_python_environment,
        }
        if manifest['manifest_type'] in builders:
            builders[manifest['manifest_type']](manifest=manifest, path=path)
            return None
        return "Error environment does not exists"

    def build(self, path, cid):
        manifest = os.path.join(path, 'manifest.json')
        logging.info("Building {}".format(cid))
        if os.path.exists(manifest):
            with open(manifest) as file:
                manifest = json.load(file)
                output = self.build_environment(manifest, path)
                logging.info("Build runner output: {}".format(output))
                if output:
                    return output
                path = os.path.join(os.path.dirname(path), '.')
                logging.warning("Cache = true, git clone won't work if updated")
                packet = self.client.build(path=path, name=cid)
                if packet.is_valid():

                    stdout = packet.data["stdout"]
                    stderr = packet.data["stderr"]
                    if stderr:
                        return stderr, True
                    return stdout, False

                return "unable to parse the packet returned by the docker host server, try again later.", False


builder = Builder()
builder.consume()
"""
