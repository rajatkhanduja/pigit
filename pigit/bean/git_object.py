from typing import Union

from abc import ABCMeta
from .enum import GitObjectType


class GitObject(metaclass=ABCMeta):
    def __init__(self, object_id: Union[str, None], object_type: GitObjectType, is_fully_loaded=False):
        super().__init__()

        if object_type is None:
            raise ValueError("'type' cannot be None")
        self.id = object_id
        self.type = object_type
        self.is_loaded = is_fully_loaded

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, other: 'GitObject'):
        return type(other) == type(self) and other.__dict__ == self.__dict__
