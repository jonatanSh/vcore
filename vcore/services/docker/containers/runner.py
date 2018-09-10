import json
from vcore.tasks.api.celery import celery_engine
from vcore.services.docker.lib.engine import docker_engine


@celery_engine.task(name="Runner.run", trail=True)
def run(**kwargs):
    if type(kwargs["ports"]) == str:
        try:
            kwargs["ports"] = json.loads(kwargs["ports"])
        except:
            raise Exception("Ports is not json serializable")
    container = docker_engine.containers.run(**kwargs)

    if hasattr(container, "attrs"):
        return {"output": container.attrs}
    return {
        "container_run_error": str(container)
    }
