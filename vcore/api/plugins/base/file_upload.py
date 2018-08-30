from flask_restful import reqparse
from werkzeug import datastructures
from vcore.tasks.api.task_objects import Task
from vcore.configuration.conf_loader import Settings
from vcore.api.backends.get_backend import get_backend, API


class UploadProvider(Task):
    def task_handle_post(self, *args, **kwargs):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=datastructures.FileStorage, location=Settings.settings.API.upload_folder)

        args = parse.parse_args()

        file = args["file"]

        file.save()

        storage_backend = get_backend(API.STORAGE)
        return {
            "file_id": storage_backend.store_archive(file.path)
        }


class DownloadProvider(Task):
    def task_handle_get(self, file_id):
        storage_backend = get_backend(API.STORAGE)

        return {
            "hex": storage_backend.get_archive(file_id).hex()
        }
