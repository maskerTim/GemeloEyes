from ..template import template
import psutil
from datetime import datetime
from logger.logger import Logger
logger = Logger.instance()

class CPUandMemoryForDM(template):
    """ Device Monitor for monitoring CPU and memory """
    def __init__(self, interval=0.5, handler=None, qos=0):
        super().__init__()
        self._interval = interval
        self._handler = handler
        self._qos = qos

    def setInterval(self, interval):
        """ set interval """
        self._interval = interval

    def setQoS(self, qos):
        """ set QoS level for publisher """
        self._qos = qos

    def _getPerformance(self):
        self._perf.append({
            # the logical number of cpu
            'cpu_count': psutil.cpu_count(),
            # percent usage of cpu
            'cpu_percent': psutil.cpu_percent(self._interval),
            # a named tuple including current, min and max frequencies expressed in Mhz
            'cpu_frequency_current': psutil.cpu_freq()[0],
            'cpu_frequency_min': psutil.cpu_freq()[1],
            'cpu_frequency_max': psutil.cpu_freq()[2],
            # percent usage of memory
            'memory_percent': psutil.virtual_memory()[2],
            # the recording time of data
            'recorded_time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })

    def _connectTo(self):
        return self._handler._connectTo()

    def _writeTo(self):
        return self._handler._writeTo(self._perf, self._qos)

    def _close(self):
        try:
            self._handler.close()
        except Exception as e:
            logger.error('closing occurs error', e)