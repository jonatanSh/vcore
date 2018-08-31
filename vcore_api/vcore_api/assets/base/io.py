from ..base_asset import Asset
from ...core.response import StreamResponse, JsonResponse


class IoAsset(Asset):
    def download(self, file_id):
        return self.requests.get(url="api/download/{0}".format(file_id), ResponseObject=StreamResponse)

    def upload(self, local_file):
        with open(local_file, "rb") as file:
            stream = file.read()
        print(stream.hex())
        return self.requests.post(url="api/upload", parameters={
            "stream": stream.hex(),
            "encoding": "hex",
        }, ResponseObject=JsonResponse)
