from abc import ABCMeta, abstractmethod
from ..bean import Tree


class WorkingArea(metaclass=ABCMeta):
    @abstractmethod
    def setup(self, snapshot: Tree):
        pass
