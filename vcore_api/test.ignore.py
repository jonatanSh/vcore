from vcore_api import Api
from vcore_api import collections
import os
from time import sleep

path = os.path.join(os.path.dirname(os.getcwd()), "test_packages", "docker")
api = Api()  # "172.16.224.128")
# output = api.docker.images.build(path)
# print(output)
#
# task = api.get_task(output.request)
# while not task.is_done():
#     sleep(1)
# task = task.async_result()
# if task.error:
#     print("Error exit", task.output)
#     exit(1)
# image_name = task.output.image_name
# print("image name:", image_name)
# print(api.docker.images.list())
#
# print("new line")
# print(api.docker.containers.list())
#
# print("new line")
#
# print(api.docker.containers.list(all=True))
#
ports = collections.PortsCollection.create_collection()

ports.add_tcp_port(15672, 15672)
ports.add_tcp_port(5672, 5672)
print(ports)
output = api.docker.containers.run(image="rabbitmq", ports=ports, detach=True, name="rabbit")
print(output)

task = api.get_task(output.request)
while not task.is_done():
    sleep(1)
print(task.async_result().output)
