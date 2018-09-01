import requests
from urllib3.exceptions import HTTPError
from .exceptions import ApiConnectionError


class Utils(object):
    @staticmethod
    def parameters_joiner(parameters):
        pstr = ""
        for key, value in parameters.items():
            pstr += "&{0}={1}".format(key, value)
        pstr = "?" + pstr[1:]
        if pstr == "?":
            return ""
        return pstr

    @staticmethod
    def mk_get_url(url, parameters):
        return "{0}{1}".format(url, Utils.parameters_joiner(parameters))

    @staticmethod
    def url_join(*pre_args):
        args = [pre_args[0]]
        for arg in pre_args[1:]:
            if arg.startswith("/"):
                arg = arg[1:]
            args.append(arg.replace("//", "/"))
        return "/".join(args)


class RequestHandler(object):
    def __init__(self, host, port):
        self.base_url = "{0}:{1}".format(host, port)

    def get(self, url, ResponseObject, parameters={}):
        url = Utils.mk_get_url(url, parameters)
        url = Utils.url_join(self.base_url, url)
        try:
            response = requests.get(url)
        except (Exception, ConnectionRefusedError, HTTPError) as error:
            raise ApiConnectionError(url, details=str(error))
        return ResponseObject(response=response, url=url, api=self)

    def post(self, url, ResponseObject, parameters={}):
        url = Utils.url_join(self.base_url, url)
        try:
            response = requests.post(url=url, data=parameters)
        except (Exception, ConnectionRefusedError, HTTPError) as error:
            raise ApiConnectionError(url, details=str(error))
        return ResponseObject(response=response, url=url, api=self)
