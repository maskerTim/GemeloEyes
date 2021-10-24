class NotSetParamError(Exception):
    """ Error for not set parameter that's needed """
    def __init__(self, value) -> None:
        self._value = value

    def __str__(self):
        return (repr(self.value))