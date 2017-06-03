class PigitException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotGitDirException(PigitException):
    def __init__(self, dir):
        super().__init__(1, "fatal: Not a git repository (or any of the parent directories): .git")
        self.dir = dir


class InvalidObjectNameException(PigitException):
    def __init__(self, object_id):
        super().__init__(2, "No such object")
        self.id = object_id


class DuplicateObjectException(PigitException):
    def __init__(self, object_id):
        super().__init__(3, "Duplicate object")
        self.id = object_id
