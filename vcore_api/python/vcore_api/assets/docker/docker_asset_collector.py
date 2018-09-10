from ..base_asset import Asset
from .images import Image
from .networks import Networks
from .containers import Containers


class DockerAssetCollector(Asset):

    @property
    def images(self):
        return Image(self.requests, self.api)

    @property
    def containers(self):
        return Containers(self.requests, self.api)

    @property
    def networks(self):
        return Networks(self.requests, self.api)

    def shell(self, container_name):
        """
        Trying to run a minimal emulated shell in the container
        :param container_name: the container name
        :return:
        """
        # lazy import this is a feature, it shouldn't break everything
        from ...lib.interactive_shell import create_shell, stop_shell

        def exec_wrapper(command):
            if command.lower() == "exit":
                stop_shell()

            response = self.containers.remote_exec(container_name, command)
            return str(response.output)

        create_shell(exec_wrapper)
