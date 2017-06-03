class Signature(object):
    def __init__(self, name: str, email: str, timestamp: int, offset_minutes: int):
        self.name = name
        self.email = email
        self.timestamp = timestamp
        self.offset_minutes = offset_minutes

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, other):
        return type(other) == type(self) and other.__dict__ == self.__dict__