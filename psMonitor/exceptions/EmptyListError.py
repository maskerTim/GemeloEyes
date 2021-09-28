class EmptyListError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self._msg = "Error for Empty List!"

    def describe(self):
        print(self._msg)