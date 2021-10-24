import abc
from exceptions.NotSetParamError import NotSetParamError

class NWSample(abc.ABC):
    """ Sample implementation of Network """

    def __init__(self, host) -> None:
        super().__init__()
        if not host:
            raise NotSetParamError('Not set the host parameter...')
        else:
            self._host = host
        self._nwHandler = None

    def setHost(self, host):
        """ set db name """
        self._host = host

    @abc.abstractmethod
    def _connectTo(self):
        """ connect to DB """
        return NotImplemented

    @abc.abstractmethod
    def _writeTo(self):
        """ write to DB"""
        return NotImplemented