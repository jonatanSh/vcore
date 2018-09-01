class ApiConnectionError(Exception):
    def __init__(self, connection_str, details):
        self.connection_str = connection_str
        self.details = details

    def __str__(self):
        return "ApiConnectionError({0}, {1})".format(self.connection_str, self.details)
