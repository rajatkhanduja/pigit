from .git_object import GitObject
from .tree import Tree
from .signature import Signature
from .enum import GitObjectType


class Commit(GitObject):
    def __init__(self, object_id: str, parents: ['Commit']=None, author: Signature=None,
                 committer: Signature=None, commit_message: str=None, tree: Tree = None,
                 is_fully_loaded=False):
        super().__init__(object_id, GitObjectType.COMMIT, is_fully_loaded)
        self.parents = parents
        self.author = author
        self.committer = committer
        self.message = commit_message
        self.tree = tree
