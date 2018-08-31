from vcore_api import Api
import os

path = os.path.join(os.path.dirname(os.getcwd()), "test_packages", "docker")
api = Api()

output = api.io.upload(path)
print(output)
