import docker
from vcore.configuration.conf_loader import Settings


def create_client():
    client = docker.DockerClient(base_url=Settings.settings.DOCKER.client_url)
    Settings.docker_engine = client


if "docker_engine" not in Settings.runtime:
    create_client()

docker_engine = Settings.runtime.docker_engine
