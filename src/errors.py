class ApiException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class SomethingIsNotRight(ApiException):
    def __init__(self):
        super().__init__("Oh no!")
