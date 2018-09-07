from flask_restful import reqparse
from vcore.tasks.api.task_objects import Task
from vcore.api.backends.get_backend import get_backend, API
from vcore.api.backends.storage.exceptions import UnknownEncoding, FileNotFound
from vcore.api.plugins.utils import api_base_wrapper, api_error


class UploadProvider(Task):
    def task_handle_post(self, *args, **kwargs):
        parse = reqparse.RequestParser()

        parse.add_argument('stream')
        parse.add_argument('encoding')
        parse.add_argument("ext")

        kwargs = parse.parse_args()

        storage_backend = get_backend(API.STORAGE)
        file_id = None
        try:
            file_id = storage_backend.store_archive(**kwargs)
        except UnknownEncoding as error:
            api_error(error)

        return api_base_wrapper({
            "file_id": file_id,
        })


class DownloadProvider(Task):
    def task_handle_get(self, file_id):
        storage_backend = get_backend(API.STORAGE)
        stream = None

        try:
            stream = storage_backend.get_archive(file_id).hex()
        except FileNotFound as error:
            return api_error(error)

        return api_base_wrapper({
            "hex": stream
        })
