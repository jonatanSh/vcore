from sqlalchemy import create_engine
from vcore.configuration.conf_loader import Settings


class Database(object):
    def __init__(self):
        self.db_connect = create_engine(Settings.settings.DATABASE.connection_string)

    def execute(self, *args, **kwargs):
        connection = self.db_connect.connect()
        connection.execute(*args, **kwargs)


database = Database()
