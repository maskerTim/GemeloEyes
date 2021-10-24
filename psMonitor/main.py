import sys
print(sys.path)

from templates.deviceMonitor.CPUandMemoryForDM import CPUandMemoryForDM
from factory.DBFactory import DBFactory
from factory.NWFactory import NWFactory
from controller.param import MonitorAgents
import os
import time

from flask import Flask
from controller.param import paramModule
import threading

from dotenv import load_dotenv
from logger.logger import Logger
logger = Logger.instance()

app = Flask(__name__)
app.register_blueprint(paramModule)

def running_server():
    logger.info('server is running...')
    app.run(host="0.0.0.0", port=3000)

@app.route('/', methods=['GET'])
def hello_world():
    """
    Testing the web server is running
    :return: message of running web server
    """
    return "Web server is running"

if __name__=='__main__':
    """ Entry point """
    # run flask server for listening
    threading.Thread(target=running_server, daemon=True).start()

    """ Monitor and write into Database """
    load_dotenv()
    logger.info('Load environment variables successfully.')
    # dbHandler = DBFactory.createInstance('sqlite3', dbName='performance.db')
    # cpuAndMemDM = CPUandMemoryForDM(handler=dbHandler)
    # while True:
    #     cpuAndMemDM.monitor()
    """ Monitor and send outside through network """
    nwHandler = NWFactory.createInstance('mqtt', host=("192.168.0.199", 1883))
    nwHandler.setTopic("Try/Test")
    cpuAndMemDM = CPUandMemoryForDM(handler=nwHandler)

    # register agent to listener
    MonitorAgents.registerSingle(('test', cpuAndMemDM))
    
    # start monitoring
    while True:
        cpuAndMemDM.monitor()

    

