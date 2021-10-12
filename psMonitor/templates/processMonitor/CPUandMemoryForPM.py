from .processMonitor import processMonitor

class CPUandMemoryForPM(processMonitor):
    """ Process Monitor for monitoring CPU and memory """
    def __init__(self, pids):
        super().__init__(pids)

    def getPerformance(self):
        pass

    def connectTo(self):
        pass

    def writeTo(self):
        pass