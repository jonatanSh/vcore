import json


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


class Response(object):
    def __init__(self, response, url, api):
        self.url = url
        self._api = api
        self._status = response.status_code
        try:
            self.response_object = response.json()
        except:
            self.response_object = {}

    def __getattr__(self, item):
        if item in [
            "is_done",
        ]:
            return super(Response, self).__getattribute__(item)

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
            return Response(value, self.url, self._api)
        else:
            return value

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
        return "Response(url={0},response={1})".format(self.url, conf)

    def __contains__(self, item):
        return item in self.response_object

    def __repr__(self):
        return str(self)

    def is_done(self):
        obj = {}
        if "is_done_url" in self:
            obj = self._api.get(url=self.is_done_url)
        if "status" in obj:
            return obj.status in [
                "SUCCESS",
                "FAILURE",
            ]
        if obj:
            return False
        return True
