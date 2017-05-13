from .enum import GitObjectType
from .git_object import GitObject


class BlobObject(GitObject):

    def __init__(self, object_id: str, content: str):
        super().__init__(object_id, GitObjectType.BLOB, content)

    def __str__(self):
        raise NotImplementedError("Need to implement this method before it can be printed")
