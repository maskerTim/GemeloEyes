import abc
from exceptions.NotSetParamError import NotSetParamError

class DBSample(abc.ABC):
    """ Sample implementation of Database """

    def __init__(self, dbName) -> None:
        super().__init__()
        if not dbName:
            raise NotSetParamError('Not set the dbname parameter...')
        else:
            self._dbName = dbName
        self._dbHandler = None

    def setDBName(self, dbName):
        """ set db name """
        self._dbName = dbName

    @abc.abstractmethod
    def _connectTo(self):
        """ connect to DB """
        return NotImplemented

    @abc.abstractmethod
    def _writeTo(self, performance):
        """ write to DB"""
        return NotImplemented