from .database.DBSqlite3 import DBSqlite3

class DBFactory():
    """ Database Factory to create different types of instance (e.g., database or netowrk) """

    @staticmethod
    def createInstance(instance, host):
        """ create some type of instance"""
        databases = {
            'sqlite3': DBSqlite3(host),
        }
        return databases[instance]