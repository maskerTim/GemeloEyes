from ..template import template

class processMonitor(template):
    """ Template for process monitor """
    def __init__(self, pids):
        self.__processes = pids # list of process IDs