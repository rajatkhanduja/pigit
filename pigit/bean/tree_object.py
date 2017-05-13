from .git_object import GitObject
from .enum import GitObjectType


class TreeObject(GitObject):

    def __init__(self, object_id: str, content: str):
        super().__init__(object_id, GitObjectType.TREE, content)

    def __str__(self):
        raise NotImplementedError("Need to implement this method before it can be printed")
