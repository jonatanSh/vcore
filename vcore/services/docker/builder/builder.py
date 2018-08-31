from vcore.tasks.api.celery import celery_engine
from vcore.services.docker.lib.engine import docker_engine


@celery_engine.task(name="Builder.build_image", trail=True)
def build_image(local_path):
    docker_engine.images.build(local_path)
