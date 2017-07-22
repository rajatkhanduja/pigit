from abc import ABCMeta, abstractmethod
from typing import Generator
from pathlib import Path

from pigit.bean import Tree


class WorkingArea(metaclass=ABCMeta):
    @abstractmethod
    def setup(self, snapshot: Tree):
        pass

    @abstractmethod
    def get_files(self) -> Generator[Path, None, None]:
        pass

    @abstractmethod
    def get_file_content(self, filename) -> bytes:
        """
        Returns the content of the file
        :param filename: 
        :return:
        :raises: FileNotFoundError 
        """
        pass
