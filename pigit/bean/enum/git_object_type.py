from enum import Enum


class GitObjectType(Enum):
    TREE = 1
    BLOB = 2
    COMMIT = 3
