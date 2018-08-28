# run each tasks depends on the service configuration
from vcore.configuration.conf_loader import Settings

TASKS = []

# importing switch
if "docker" in Settings.settings.ENABLED_SERVICES:
    from vcore.tasks.services.docker.tasks import TASKS as DOCKER_TASKS

    TASKS += DOCKER_TASKS
