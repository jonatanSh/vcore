import os
from vcore.tasks.api.celery import celery_engine
from vcore.services.docker.lib.engine import docker_engine
from vcore.lib.io import TempArchive
from vcore.lib.utils import local_path


@celery_engine.task(name="Builder.build_image", trail=True)
def build_image(file_id, target):
    with TempArchive(local_path(file_id)) as docker_directory:
        image, output = docker_engine.images.build(path=docker_directory, target=target)
        output = list(output)[0]
        output_lst = [

        ]
        for key, line in output.items():
            output_lst.append(line)

        return {
            "output": output_lst,
            "image_name": image.tags[0],
            "id": image.id
        }
