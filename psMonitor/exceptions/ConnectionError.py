class ConnectionError(Exception):
    """ connection is error"""
    def __init__(self, value) -> None:
        self._value = value

    def __str__(self):
        return (repr(self.value))