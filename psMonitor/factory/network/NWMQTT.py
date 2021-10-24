from .NWSample import NWSample
from exceptions.NotSetParamError import NotSetParamError
import paho.mqtt.client as mqtt
import json

from logger.logger import Logger
logger = Logger.instance()

class NWMQTT(NWSample):
    """ MQTT Instance """

    def __init__(self, host) -> None:
        super().__init__(host)
        self._topic = None
        self._nwHandler = mqtt.Client()

    def setTopic(self, topic):
        self._topic = topic

    def _connectTo(self):
        try:
            self._nwHandler.connect(self._host[0], self._host[1])
            logger.info("mqtt connection is successful")
        except Exception:
            logger.error("mqtt connection occurs error")
            return False
        return True

    def _writeTo(self, performance):
        if not self._topic:
                raise NotSetParamError("not set topic parameter...")
        try:
            self._nwHandler.publish(self._topic, json.dumps(performance))
            logger.info('message is successfully published...')
        except Exception:
            logger.error("mqtt writting occurs error...")
            return False
        return True
