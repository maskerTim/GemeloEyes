
from flask import Blueprint, request, jsonify
paramModule = Blueprint('param', __name__)

from exceptions.NotSetParamError import NotSetParamError
from logger.logger import Logger
logger = Logger.instance()

class MonitorAgents():
    """ Monitor Agent for the task monitoring the performance """
    _registerAgent = {}

    def __init__(self) -> None:
        pass

    @classmethod
    def registerMultiple(cls, agents):
        """ Agent parameter is tuple, (name, instance of monitor) and this method for registering more than one agent """
        if not agents or len(agents)==0:
            raise NotSetParamError('not set agents...')

        for agent in agents:
            cls._registerAgent[agent[0]] = agent[1]
            logger.info('registered:'+agent[0])

    @classmethod
    def registerSingle(cls, agent):
        """ Agent is tuple, (name, instance of monitor) and this method for registering only single agent """
        if not agent:
            raise NotSetParamError('not set agents...')
        cls._registerAgent[agent[0]] = agent[1]
        logger.info('registered:'+agent[0])

    @classmethod
    def searchAgent(cls, name):
        """ search Agent that is registered """
        if name not in cls._registerAgent:
            return False
        return cls._registerAgent[name]
        


@paramModule.route('/changeInterval/<string:name>/interval/<float:interval>', methods=['POST'])
def changeInterval(name, interval):
    """ set interval parameter of some monitor agent """
    # search agent exists or not
    agent = MonitorAgents.searchAgent(name)
    # if yes, set interval
    if agent:
        agent.setInterval(interval)
    else:
        return "Fail to search agent..."
    return "Successful to set interval of agent..."