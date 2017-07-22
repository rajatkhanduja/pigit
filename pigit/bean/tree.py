from typing import Union

from .git_object import GitObject
from .tree_entry import TreeEntry
from .enum import GitObjectType


class Tree(GitObject):
    def __init__(self, object_id: Union[str, None] = None, entries:[TreeEntry] = None):
        super().__init__(object_id, GitObjectType.TREE)
        if entries is None:
            entries = []
        self.entries = entries

    def add_entry(self, entry: TreeEntry):
        self.entries.append(entry)
