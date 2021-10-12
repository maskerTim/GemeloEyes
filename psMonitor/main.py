import sys
print(sys.path)

from templates.deviceMonitor.CPUandMemoryForDM import CPUandMemoryForDM
import os
import time

from dotenv import load_dotenv
from logger.logger import Logger
logger = Logger.instance()

if __name__=='__main__':
    """ Entry point """
    load_dotenv()
    logger.info('Load environment variables successfully.')
    cpuAndMemDM = CPUandMemoryForDM()
    while True:
        cpuAndMemDM.monitor()
