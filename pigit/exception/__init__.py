from pigit.bean.enum import SpecialReference


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


class NoSuchSpecialReferenceException(PigitException):
    def __init__(self):
        super().__init__(4, "No HEAD file found")


class NoSuchReferenceException(PigitException):
    def __init__(self, reference: str):
        super().__init__(5, "No such reference")
        self.reference = reference


class NoSuchBranchException(PigitException):
    def __init__(self, branch: str):
        super().__init__(6, "No such branch")
        self.branch = branch


class ObjectDirDoesNotExistException(PigitException):
    def __init__(self, dir):
        super().__init__(7, "Object directory {dir} not found".format(dir=dir))
        self.dir = dir


class IndexNotFoundException(PigitException):
    def __init__(self):
        super().__init__(8, "Index not found or does not exist")


class IndexCorruptedException(PigitException):
    def __init__(self, code=9, message="Index is corrupted"):
        super().__init__(code, message)


class IndexChecksumDoesNotMatchException(IndexCorruptedException):
    def __init__(self, expected, calculated):
        super().__init__(10, "Index checksum does not match")
        self.expected = expected
        self.calculated = calculated


class BranchNameNotRecognizedException(PigitException):
    def __init__(self, name: str):
        super().__init__(11, "Could not recognize branch by name : " + name)
        self.name = name


class ReferenceAlreadyExistsException(PigitException):
    def __init__(self, reference_name):
        super().__init__(12, "Reference already exists in store : " + reference_name)
        self.name = reference_name


class SpecialReferenceNotSetException(PigitException):
    def __init__(self, reference: SpecialReference):
        super().__init__(13, f"{reference} is not set yet")


class NothingToCommitException(PigitException):
    def __init__(self):
        super().__init__(14, "Nothing to commit")