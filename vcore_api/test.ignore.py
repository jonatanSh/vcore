from vcore_api import Api
import os
from time import sleep

path = os.path.join(os.path.dirname(os.getcwd()), "test_packages", "docker")
api = Api()

output = api.docker.image.build(path)
while not output.is_done():
    sleep(1)
print(output.async_result())
