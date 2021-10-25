from .network.NWMQTT import NWMQTT

class NWFactory():
    """ Network Factory to create different types of instance (e.g., database or netowrk) """

    @staticmethod
    def createInstance(instance, host):
        """ create some type of instance return Tuple"""
        networks = {
            'mqtt': NWMQTT(host),
        }
        return networks[instance]