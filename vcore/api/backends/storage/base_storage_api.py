class StorageApiInterface(object):
    def store_archive(self, local_path):
        """
        Return the archive id
        :param local_path:
        :return:
        """
        raise NotImplemented()

    def get_archive(self, archive_id):
        """
        Return as a file binary stream
        :return:
        """
        raise NotImplemented()
