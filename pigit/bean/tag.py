from typing import Union

from .git_object import GitObject
from .signature import Signature
from .enum import GitObjectType


class Tag(GitObject):
    def __init__(self, object_id: Union[str, None], name: str, tagger: Signature, target: str, target_type: GitObjectType,
                 message: str):
        super().__init__(object_id, GitObjectType.TAG)
        self.name = name
        self.tagger = tagger
        self.target = target
        self.target_type = target_type
        self.message = message
