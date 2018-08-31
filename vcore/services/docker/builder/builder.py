from vcore.tasks.api.celery import celery_engine
from vcore.services.docker.lib.engine import docker_engine
from vcore.lib.io import TempArchive
from vcore.lib.utils import local_path


@celery_engine.task(name="Builder.build_image", trail=True)
def build_image(file_id):
    with TempArchive(local_path(file_id)) as docker_directory:
        docker_engine.images.build(docker_directory)
