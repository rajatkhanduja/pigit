from typing import Union

from .enum import GitObjectType
from .git_object import GitObject


class Blob(GitObject):

    def __init__(self, object_id: Union[str, None], content: bytes, is_fully_loaded=True):
        super().__init__(object_id, GitObjectType.BLOB, is_fully_loaded)
        self.content = content
