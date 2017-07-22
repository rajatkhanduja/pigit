from abc import ABCMeta, abstractmethod
from pathlib import Path

from pigit.bean import Index


class StagingArea(metaclass=ABCMeta):

    @abstractmethod
    def get_index(self) -> Index:
        """
        Method to get Index object. 
        :return: Index
        :raises: IndexCorruptedException, IndexNotFoundException
        """
        pass


    @abstractmethod
    def add_to_index(self, file: Path, hash: str):
        pass