from abc import ABCMeta, abstractmethod
from ..bean import GitObject, Commit


class ObjectStore(metaclass=ABCMeta):

    @abstractmethod
    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        pass

    @abstractmethod
    def store_object(self, object: GitObject):
        pass
