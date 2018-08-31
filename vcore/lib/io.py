import shutil
import tempfile


class TempArchive(object):
    def __init__(self, local_path):
        self.local_path = local_path
        self.temp_directory = tempfile.mkdtemp()

    def __enter__(self):
        shutil.unpack_archive(self.local_path, self.temp_directory)
        return self.temp_directory

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.temp_directory)
