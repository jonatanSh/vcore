class UnknownEncoding(Exception):
    def __init__(self, encoding):
        self.encoding = encoding

    def __str__(self):
        return "UnknownEncoding({0})".format(self.encoding)


class FileNotFound(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "FileNotFound({0})".format(self.path)
