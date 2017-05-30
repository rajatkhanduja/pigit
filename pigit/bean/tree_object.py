from .git_object import GitObject
from .enum import GitObjectType


class TreeObject(GitObject):
    def __init__(self, object_id: str):
        super().__init__(object_id, GitObjectType.TREE)
        self.children = []

    def add_child(self, node: GitObject):
        self.children.append(node)

    def __str__(self):
        raise NotImplementedError("Need to implement this method before it can be printed")

    def dictonary_for_representation(self):
        data = super(TreeObject, self).dictonary_for_representation()
        data['children'] = self.children
        return data
