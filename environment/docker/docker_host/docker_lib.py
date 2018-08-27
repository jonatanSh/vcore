import subprocess
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from environment.utils.logger import get_logger

logger = get_logger(__file__)


class DockerClass(object):
    def build(self, path, name, cache=True):
        args = []
        if not cache:
            args.append("--no-cache")

        if args:
            base_cmd = "docker build {}".format(",".join(args))
        else:
            base_cmd = "docker build"
        cmd = "{base} {path} -t {name}".format(base=base_cmd, path=path, name=name).split(" ")

        return self.generic_run(cmd)

    def run(self, name, port):
        cmd = "docker run -d -p {port}:{port} {name} node gritty/bin/gritty.js --port {port}".format(
            name=name,
            port=port)
        try:
            return {"output": self.generic_run(cmd), "cmd": cmd}
        except Exception as error:
            return {"output": error, "cmd": cmd}

    @staticmethod
    def generic_run(cmd):
        if type(cmd) is str:
            cmd = cmd.split(" ")
        logger.info("GenericRun.cmd => {0}".format(cmd))
        stdout, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        logger.info("GenericRun.output => stdout={0}, stderr={1}".format(stdout, stderr))
        return {
            "data": {
                "stdout": stdout.decode("utf-8"),
                "stderr": stderr.decode("utf-8")
            }
        }


Docker = DockerClass()


def docker_factory(request):
    try:
        return getattr(Docker, request.action)(*request.args, **request.kwargs)
    except Exception as error:
        return str(error)


DockerHandler = docker_factory
