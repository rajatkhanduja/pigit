from datetime import datetime

from .git_object import GitObject
from .enum import GitObjectType


class CommitObject(GitObject):
    def __init__(self, object_id: str, parent: 'CommitObject', parent_id: str, tree_ref: str = None, author: str = None,
                 author_email: str = None, author_timestamp: datetime = None, committer: str = None,
                 committer_email: str = None, commit_timestamp: datetime = None, commit_message: str = None,
                 is_fully_loaded=False):
        super().__init__(object_id, GitObjectType.COMMIT, is_fully_loaded)
        self.parent = parent
        self.parent_id = parent_id
        self.author = author
        self.author_email = author_email
        self.author_timestamp = author_timestamp
        self.committer = committer
        self.committer_email = committer_email
        self.commit_timestamp = commit_timestamp
        self.commit_message = commit_message
        self.tree_reference = tree_ref

    def dictonary_for_representation(self):
        data = super(CommitObject, self).dictonary_for_representation()
        data['author'] = self.author
        data['committer'] = self.committer
        data['author_timestamp'] = self.author_timestamp
        data['commit_timestamp'] = self.commit_timestamp
        data['parent_id'] = self.parent_id
        data['commit_message'] = self.commit_message
        data['tree_reference'] = self.tree_reference
        if self.is_loaded:
            data['parent'] = self.parent.dictonary_for_representation()
        return data
