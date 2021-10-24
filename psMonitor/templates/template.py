import abc
from exceptions.ConnectionError import ConnectionError

class template(abc.ABC):
    """ template for performance monitor """
    def __init__(self):
        super().__init__()
        self._perf = [] # performance data
        self._handler = None
        self._connected = False # the flag that checks the connection is successful or not

    @abc.abstractmethod
    def _getPerformance(self):
        """ return system performance """
        return NotImplemented

    @abc.abstractmethod
    def _connectTo(self):
        """ connect to third-party services """
        return NotImplemented

    @abc.abstractmethod
    def _writeTo(self):
        """ write to third-party storage """
        return NotImplemented

    @abc.abstractmethod
    def _close(self):
        """ close connection """
        return NotImplemented

    def _isConnected(self):
        """ check connection is successful """
        return self._connected

    def _clear(self):
        """ clear the previous performance data """
        self._perf.clear()

    def monitor(self):
        """ monitor system performance """
        self._getPerformance()
        if not self._isConnected():
            result = self._connectTo()
            if not result:
                raise ConnectionError('connection occurs error...')
            self._connected = True
        self._writeTo()
        self._clear()

    def test_monitor(self, func_name):
        """ monitor system performance for test """
        if func_name=='getPerformance':
            self._getPerformance()
            return self._perf
        elif func_name=='writeTo':
            self._connectTo()
            self._writeTo()
        elif func_name=='clear':
            return self._perf
        elif func_name=='close':
            self._close()
        