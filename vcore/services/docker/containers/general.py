from vcore.services.docker.lib.engine import docker_engine


def exec_command(container, command):
    container = docker_engine.containers.get(container)
    output = container.exec_run(command)
    return {
        "output": output.output.decode("utf-8"),
        "exit_code": output.exit_code
    }
