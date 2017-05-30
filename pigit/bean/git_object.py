from abc import ABCMeta
from .enum import GitObjectType


class GitObject(metaclass=ABCMeta):
    def __init__(self, object_id: str, object_type: GitObjectType, is_fully_loaded=False):
        super().__init__()
        self.id = object_id
        self.type = object_type
        self.is_loaded = is_fully_loaded

    def dictonary_for_representation(self):
        return {
            'id': self.id,
            'type': self.type,
            'is_loaded': self.is_loaded
        }

    def __repr__(self):
        return repr(self.dictonary_for_representation())
