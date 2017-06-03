from .git_object import GitObject
from .enum import GitObjectType


class Tree(GitObject):
    def __init__(self, object_id: str):
        super().__init__(object_id, GitObjectType.TREE)
        self.children = []

    def add_child(self, node: GitObject):
        self.children.append(node)

