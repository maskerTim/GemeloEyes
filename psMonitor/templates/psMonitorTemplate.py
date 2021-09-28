import abc
import psutil

# Declare this is abstract class
class psMonitorTemplate(abc.ABC):
    """ Template for monitoring process """
    def __init__(self, pids) -> None:
        super().__init__()
        self._processes = [] # list of processes
        for p in pids:
            self._processes.append(psutil.Process(p))
        self._perf = [] # performance data of multiple processes
        self._DBclient = None # the client controller for DB

    @abc.abstractmethod
    def getPerformance(self):
        """ return system performance """
        return NotImplemented

    @abc.abstractmethod
    def connectToDB(self):
        """ connect to DB """
        return NotImplemented

    @abc.abstractmethod
    def writeToDB(self):
        """ write data into db """
        return NotImplemented

    def clearData(self):
        """ clear data after writing data into DB """
        self._perf.clear()

    def monitor(self):
        """ monitor the process performance """
        self.getPerformance()
        if not self._DBclient:
            self.connectToDB()
        self.writeToDB()
        self.clearData()
        
