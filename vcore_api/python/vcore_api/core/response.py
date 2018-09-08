import json
from io import BytesIO


class ResponseAttributeError(Exception):
    def __init__(self, error_message, obj):
        self.error_message = error_message
        if type(obj) is dict:
            try:
                obj = json.dumps(obj, indent=2)
            except Exception:
                pass

        self.obj = obj

    def __str__(self):
        return "AttributeError: {0}, in {1}".format(self.error_message, self.obj)


class JsonResponse(object):
    def __init__(self, response, url, api):
        self.url = url
        self._api = api
        if "status_code" in response:
            self._status = response.status_code
        else:
            self._status = "inner_object"
        self._last_is_done = {}
        try:
            self.response_object = response.json()
        except:
            self.response_object = response

    def __getattr__(self, item):
        if item in [
            "is_done",
            "async_result",
            "_last_is_done",
            "_api",
            "url",
            "_status",
        ]:
            return super(JsonResponse, self).__getattribute__(item)

        if type(self.response_object) is dict:
            try:
                value = self.response_object[item]
            except (Exception, AttributeError):
                raise ResponseAttributeError(item, self.response_object)
        else:
            if hasattr(self.response_object, item):
                value = getattr(self.response_object, item)
            else:
                raise ResponseAttributeError(item, self.response_object)
        if type(value) is dict:
            return JsonResponse(value, self.url, self._api)
        else:
            return value

    def __setitem__(self, key, value):
        if type(self.response_object) is dict:
            self.response_object[key] = value
        else:
            setattr(self.response_object, key, value)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        try:
            conf = json.dumps(
                self.response_object,
                indent=2
            )
        except Exception:
            conf = self.response_object
        return "JsonResponse(url={0},status={1},response={2})".format(self.url, self._status, conf)

    def __contains__(self, item):
        return item in self.response_object

    def __repr__(self):
        return str(self)

    def is_done(self):
        obj = {}
        if "is_done_url" in self:
            obj = self._api.get(url=self.is_done_url, ResponseObject=JsonResponse)
            self._last_is_done = obj
        if "status" in obj:
            return obj.status in [
                "SUCCESS",
                "FAILURE",
            ]
        if obj:
            return False
        return True

    def async_result(self):
        if self.is_done():
            return self._last_is_done


class StreamResponse(object):
    def __init__(self, response, url, api):
        self.url = url
        self._api = api
        self._status = response.status_code

        try:
            self.stream = BytesIO(bytes.fromhex(response.json()["hex"]))
        except:
            self.stream = BytesIO()

    def seek(self, *args, **kwargs):
        self.stream.seek(*args, **kwargs)

    def read(self):
        return self.stream.read()

    def save(self, local_path):
        with open(local_path, "wb") as local_file:
            local_file.write(self.read())

    def __str__(self):
        return "StreamResponse(status={0}, url={1})".format(self._status, self.url)
