from abc import ABCMeta, abstractmethod
from pigit.bean import GitObject


class ObjectStore(metaclass=ABCMeta):

    @abstractmethod
    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        pass

    @abstractmethod
    def store_object(self, object: GitObject):
        pass
