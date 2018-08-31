class StorageApiInterface(object):
    def store_archive(self, local_path=None, stream=None, encoding=None):
        """
        Return the archive id
        :param local_path:
        :param stream:
        :param encoding:
        :return:
        """
        raise NotImplemented()

    def get_archive(self, archive_id):
        """
        Return as a file binary stream
        :return:
        """
        raise NotImplemented()
