from vcore_api import Api
import os

path = os.path.join(os.path.dirname(os.getcwd()), "test.txt")
api = Api()

stream = api.io.download("1")

stream.save(path)

output = api.io.upload(path)
print(output)
