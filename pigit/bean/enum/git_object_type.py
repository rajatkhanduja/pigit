from enum import Enum


class GitObjectType(Enum):
    TREE = 'tree'
    BLOB = 'blob'
    COMMIT = 'commit'
