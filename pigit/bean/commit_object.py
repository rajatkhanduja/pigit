from datetime import datetime

from .git_object import GitObject
from .git_signature import GitSignature
from .enum import GitObjectType


class CommitObject(GitObject):
    def __init__(self, object_id: str, parent: 'CommitObject', parent_id: str, tree_ref: str = None, author: str = None,
                 author_email: str = None, author_timestamp: str = None, committer: str = None,
                 committer_email: str = None, commit_timestamp: str = None, commit_message: str = None,
                 is_fully_loaded=False):
        super().__init__(object_id, GitObjectType.COMMIT, is_fully_loaded)
        self.parent = parent
        self.parent_id = parent_id
        self.author = GitSignature.from_string_timestamp(author, author_email, author_timestamp)
        self.committer = GitSignature.from_string_timestamp(committer, committer_email, commit_timestamp)
        self.commit_message = commit_message
        self.tree_reference = tree_ref
