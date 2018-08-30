import os
from uuid import uuid4
from vcore.configuration.conf_loader import Settings
from vcore.api.backends.storage.base_storage_api import StorageApiInterface

UPLOAD_DIR = Settings.settings.DISK_API_SETTINGS["directory"]


class DiskApi(StorageApiInterface):
    def get_archive(self, archive_id):
        with open(os.path.join(UPLOAD_DIR, archive_id), "rb") as archive:
            return archive.read()

    def store_archive(self, local_path):
        archive_id = str(uuid4())
        while os.path.exists(archive_id):
            archive_id = str(uuid4())
        with open(local_path, "rb") as remote_file:
            with open(os.path.join(UPLOAD_DIR, archive_id), "wb") as local_file:
                local_file.write(remote_file.read())

        return archive_id


def create_api():
    if not os.path.isdir(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)
    return DiskApi()
