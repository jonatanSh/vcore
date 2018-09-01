from vcore_api import Api

import os
from time import sleep

path = os.path.join(os.path.dirname(os.getcwd()), "test_packages", "docker")
api = Api()
"""output = api.docker.images.build(path)
print(output)

task = api.get_task(output.request)
while not task.is_done():
    sleep(1)
print(task.async_result())
"""
print(api.docker.images.list())

print("new line")
print(api.docker.containers.list())

print("new line")

print(api.docker.containers.list(all=True))
