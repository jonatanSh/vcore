from ..base_asset import Asset
from ...core.response import StreamResponse


class IoAsset(Asset):
    def download(self, file_id):
        return self.requests.get(url="api/download/{0}".format(file_id), ResponseObject=StreamResponse)

    def upload(self, local_file):
        pass
