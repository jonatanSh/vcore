from vcore_api import Api

api = Api()

stream = api.io.download("1")

stream.save("test.txt")
