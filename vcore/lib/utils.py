import os
from vcore.configuration.conf_loader import Settings


def local_path(file_id):
    return os.path.join(Settings.settings.API.upload_folder, file_id)
