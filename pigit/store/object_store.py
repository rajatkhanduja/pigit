from abc import ABCMeta, abstractmethod
from typing import Generator

from pigit.bean import GitObject


class ObjectStore(metaclass=ABCMeta):

    @abstractmethod
    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        """
        
        :param object_id: 
        :param lazy_load: 
        :return: GitObject
        :raises: InvalidObjectNameException
        """
        pass

    @abstractmethod
    def store_object(self, object: GitObject):
        """
        :param object: 
        :return:
        :raises: DuplicateObjectException 
        """
        pass

    @abstractmethod
    def get_all_objects(self) -> Generator[GitObject, None, None]:
        pass

    @abstractmethod
    def delete_object(self, object_id: str):
        pass
