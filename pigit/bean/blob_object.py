from .enum import GitObjectType
from .git_object import GitObject


class BlobObject(GitObject):

    def __init__(self, object_id: str, content: str, is_fully_loaded=True):
        super().__init__(object_id, GitObjectType.BLOB, is_fully_loaded)
        self.content = content

    def __str__(self):
        return self.content
