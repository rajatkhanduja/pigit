from abc import ABCMeta, abstractmethod
from .enum import GitObjectType


class GitObject(metaclass=ABCMeta):

    def __init__(self, object_id: str, object_type: GitObjectType, content: str):
        super().__init__()
        self.id = object_id
        self.type = object_type
        self.content = content

    @abstractmethod
    def __str__(self):
        pass