from ..template import template
import psutil
import sqlite3
from datetime import datetime
from logger.logger import Logger
logger = Logger.instance()

class CPUandMemoryForDM(template):
    """ Device Monitor for monitoring CPU and memory """
    def __init__(self, interval=0.5, dbName='performance.db'):
        super().__init__()
        self._interval = interval
        self._dbName = dbName
        self._dbHandler = None

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
        try:
            self._dbHandler = sqlite3.connect(self._dbName)
            logger.info('sqlite connection succeeds')
            # check the table exists or not, if not, create a table
            cursor = self._dbHandler.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='device_performance' ''')
            if cursor.fetchone()[0]==0:
                self._dbHandler.execute('''CREATE TABLE IF NOT EXISTS device_performance 
                    (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
                    cpu_count INT NOT NULL,
                    cpu_percent FLOAT     NOT NULL,
                    cpu_frequency_current FLOAT NOT NULL,
                    cpu_frequency_min FLOAT NOT NULL,
                    cpu_frequency_max FLOAT NOT NULL,
                    memory_percent FLOAT NOT NULL,
                    recorded_time TEXT NOT NULL);''')
                logger.info('create table successfully')
                self._dbHandler.commit()
        except Exception as e:
            logger.error('sqlite error', e)
            return False
        return True

    def _writeTo(self):
        try:
            self._dbHandler.execute('''INSERT INTO device_performance(cpu_count, cpu_percent,
                cpu_frequency_current, cpu_frequency_min, cpu_frequency_max, memory_percent, recorded_time)
                VALUES (?,?,?,?,?,?,?)''',
                [self._perf[0]['cpu_count'],
                self._perf[0]['cpu_percent'],
                self._perf[0]['cpu_frequency_current'],
                self._perf[0]['cpu_frequency_min'],
                self._perf[0]['cpu_frequency_max'],
                self._perf[0]['memory_percent'],
                self._perf[0]['recorded_time']])
            self._dbHandler.commit()
            logger.info('write into DB successfully')
        except Exception as e:
            logger.error('writing DB occurs some error', e)

    def _close(self):
        try:
            self._dbHandler.close()
        except Exception as e:
            logger.error('closing occurs error', e)