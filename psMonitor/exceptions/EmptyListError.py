class EmptyListError(Exception):
    """ Empty list exception """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self._msg = "Error for Empty List!"

    def exception(self):
        return self._msg