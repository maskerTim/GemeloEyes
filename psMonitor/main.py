import sys
print(sys.path)

from templates.CPUMemTemplate import CPUMemTemplate
import time

from dotenv import load_dotenv
from logger.logger import Logger
logger = Logger.instance()

if __name__=='__main__':
    """ Entry point """
    load_dotenv()
    logger.info('Load environment variables successfully.')
    ps = CPUMemTemplate([1999], 0.5)
    while True:
        ps.monitor()
        #time.sleep(2)
