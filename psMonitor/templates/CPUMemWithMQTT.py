from .psMonitorTemplate import psMonitorTemplate
from exceptions.EmptyListError import EmptyListError
import psutil
import os
from logger.logger import Logger
import paho.mqtt.client as mqtt
import json
logger = Logger.instance()

class CPUMemWithMQTT(psMonitorTemplate):
    """ Monitor CPU and Mem """
    def __init__(self, pids, interval=0.5, qos=1) -> None:
        super().__init__(pids)
        self._interval = interval # time interval to monitor cpu
        self._qos = qos # quality of service for MQTT

    def getPerformance(self):
        """ get processes' cpu and memory """
        # check list of the processes is empty or not
        if len(self._processes) == 0:
            logger.error('There is no process in args...')
            raise EmptyListError

        for ps in self._processes:
            payloads = {
                'pid':ps.pid,
                'name':ps.name(),
                'cpu_usage':ps.cpu_percent(self._interval),
                'mem_usage':ps.memory_info()[0]/psutil.virtual_memory()[0]
                }
            self._perf.append(payloads)

    def connectToNetwork(self):
        """ connect to mqtt broker """
        MQTT_HOST= os.getenv('MQTT_HOST')
        MQTT_PORT= int(os.getenv('MQTT_PORT'))
        self._socketclient = mqtt.Client()
        self._socketclient.connect(MQTT_HOST, MQTT_PORT)

    def writeToNetwork(self):
        """ write data into mqtt broker """
        MQTT_TOPICS= 'Performance/CPUAndMemory'
        self._socketclient.publish(MQTT_TOPICS, json.dumps(self._perf), self._qos)

    def writeToDB(self):
        return super().writeToDB()

    def connectToDB(self):
        return super().connectToDB()