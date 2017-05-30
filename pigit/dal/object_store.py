from abc import ABCMeta, abstractmethod
from ..bean import GitObject, CommitObject


class ObjectStore(metaclass=ABCMeta):

    @abstractmethod
    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        pass

    @abstractmethod
    def store_object(self, object: GitObject):
        pass

    @abstractmethod
    def get_commit(self, commit_id) -> CommitObject:
        pass

    @abstractmethod
    def get_snapshot(self, tree_reference):
        pass