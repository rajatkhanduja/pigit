class TreeEntry(object):
    def __init__(self, mode, filename: str, object_id: str):
        self.mode = mode
        self.filename = filename
        self.object_id = object_id

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, other):
        return type(other) == type(self) and other.__dict__ == self.__dict__
