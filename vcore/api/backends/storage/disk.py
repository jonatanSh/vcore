import os
from uuid import uuid4
from vcore.configuration.conf_loader import Settings
from vcore.api.backends.storage.base_storage_api import StorageApiInterface
from vcore.api.backends.storage.exceptions import UnknownEncoding, FileNotFound

UPLOAD_DIR = Settings.settings.DISK_API_SETTINGS["directory"]


def encode(stream, encoding):
    if encoding == "hex":
        return bytes.fromhex(stream)

    raise UnknownEncoding(encoding)


class DiskApi(StorageApiInterface):
    def get_archive(self, archive_id):
        path = os.path.join(UPLOAD_DIR, archive_id)
        if not os.path.exists(path):
            raise FileNotFound(archive_id)  # don't use full path for security reasons !

        with open(path, "rb") as archive:
            return archive.read()

    def store_archive(self, local_path=None, stream=None, encoding=None, ext=None):
        archive_id = str(uuid4()) + ext
        while os.path.exists(archive_id):
            archive_id = str(uuid4())

        if local_path:
            with open(local_path, "rb") as remote_file:
                stream = remote_file.read()

        with open(os.path.join(UPLOAD_DIR, archive_id), "wb") as local_file:
            if encoding:
                stream = encode(stream, encoding)
            local_file.write(stream)

        return archive_id


def create_api():
    if not os.path.isdir(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)
    return DiskApi()
