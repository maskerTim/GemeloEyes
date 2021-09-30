import sys
print(sys.path)

from templates.CPUMemWithInfluxDB import CPUMemWithInfluxDB
from templates.CPUMemWithMQTT import CPUMemWithMQTT
import os
import time

from dotenv import load_dotenv
from logger.logger import Logger
logger = Logger.instance()

if __name__=='__main__':
    """ Entry point """
    load_dotenv()
    logger.info('Load environment variables successfully.')
    multiple_process_pid = [int(x) for x in os.getenv('MULTIPLE_PROCESS_ID').split(',')]
    """ InfluxDB version """
    # ps = CPUMemWithInfluxDB(multiple_process_pid, 0.5)
    # while True:
    #     ps.monitorWithDB()
    #     #time.sleep(2)
    """ MQTT version """
    ps = CPUMemWithMQTT(multiple_process_pid, 0.5)
    while True:
        ps.monitorThroughNetwork()
        #time.sleep(2)
