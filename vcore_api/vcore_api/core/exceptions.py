class ApiConnectionError(Exception):
    def __init__(self, connection_str, details):
        self.connection_str = connection_str
        self.details = details

    def __str__(self):
        return "ApiConnectionError({0}, {1})".format(self.connection_str, self.details)


class GeneralApiError(Exception):
    def __init__(self, response, details):
        self.response = response
        self.details = details

    def __str__(self):
        return "GeneralApiError(response={0}, details={1})".format(self.response, self.details)


class IncompatibleObject(Exception):
    def __init__(self, details):
        self.details = details

    def __str__(self):
        return "IncompatibleObject({0})".format(self.details)
