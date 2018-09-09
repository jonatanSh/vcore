from vcore.services.docker.lib.engine import docker_engine


class NetWorkManager(object):
    @staticmethod
    def create(name, driver, options, ipam, check_duplicate, internal, labels, enable_ipv6, attachable, scope, ingress,
               **kwargs):
        network = docker_engine.networks.create(
            name=name,
            driver=driver,
            options=options,
            ipam=ipam,
            check_duplicate=check_duplicate,
            internal=internal,
            labels=labels,
            enable_ipv6=enable_ipv6,
            attachable=attachable,
            scope=scope,
            ingress=ingress

        )
        return network.attrs
