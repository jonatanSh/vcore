import os
from ..assets.base_asset import Asset
from ..core.response import StreamResponse, JsonResponse
from ..utils import Archive


class IoAsset(Asset):
    def download(self, file_id):
        return self.requests.get(url="api/download/{0}".format(file_id), ResponseObject=StreamResponse)

    def upload(self, local_path=None, fp=None):
        if local_path:
            if os.path.isdir(local_path):
                with Archive(local_path) as file_object:
                    stream = file_object.read()
                    local_path = file_object.name
            else:
                with open(local_path, "rb") as file:
                    stream = file.read()
        else:
            stream = fp.read()
            local_path = fp.name
        file_path, ext = os.path.splitext(local_path)
        return self.requests.post(url="api/upload", parameters={
            "stream": stream.hex(),
            "encoding": "hex",
            "ext": ext,
        }, ResponseObject=JsonResponse)
