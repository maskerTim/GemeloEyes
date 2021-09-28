from .psMonitorTemplate import psMonitorTemplate
from exceptions.EmptyListError import EmptyListError
from influxdb import InfluxDBClient
import psutil
import os
from logger.logger import Logger
logger = Logger.instance()

class CPUMemTemplate(psMonitorTemplate):
    """ Monitor CPU and Mem """
    def __init__(self, pids, interval=0.5) -> None:
        super().__init__(pids)
        self._interval = interval # time interval to monitor cpu
    
    def getPerformance(self):
        """ get processes' cpu and memory """
        # check list of the processes is empty or not
        if len(self._processes) == 0:
            logger.error('There is no process in args...')
            raise EmptyListError

        for ps in self._processes:
            self._perf.append({
                'measurement': "CPUandMem",
                'tags':{
                    'pid': ps.pid,
                    'name': ps.name()
                },
                'fields': {
                    'cpu_usage': ps.cpu_percent(self._interval),
                    'mem_usage': ps.memory_info()[0]/psutil.virtual_memory()[0]
                }
            })

    def connectToDB(self):
        """ connect to influxDB """
        DB_HOST = os.getenv('InfluxDB_HOST')
        DB_PORT = int(os.getenv('InfluxDB_PORT'))
        DB_USER = os.getenv('InfluxDB_USER')
        DB_PASSWORD = os.getenv('InfluxDB_PASSWORD')
        DB_NAME = 'CPUMem'

        self._DBclient = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
        if {'name':DB_NAME} not in self._DBclient.get_list_database():
            self._DBclient.create_database(DB_NAME)
            self._DBclient.switch_database(DB_NAME)
        else:
            self._DBclient = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        logger.info('Connect to InfluxDB successfully')

    def writeToDB(self):
        """ write data into influxDB """
        if self._DBclient.write_points(self._perf):
            logger.info('Write the datas successfully')
        else:
            logger.error('Fail to write into DB')