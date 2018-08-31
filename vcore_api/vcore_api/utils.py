from shutil import make_archive
import os
from uuid import uuid4


class Archive(object):
    def __init__(self, path):
        self.path = path
        self.archive_path = None
        self.file_object = None

    def __enter__(self):
        archive_path = str(uuid4())
        make_archive(archive_path, "zip", self.path)
        archive_path += ".zip"
        self.archive_path = archive_path
        self.file_object = open(self.archive_path, "rb")
        return self.file_object

    def __exit__(self, *args):
        os.remove(self.archive_path)
        self.file_object.close()
