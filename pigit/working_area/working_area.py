from abc import ABCMeta, abstractmethod


class WorkingArea(metaclass=ABCMeta):
    @abstractmethod
    def setup(self, snapshot):
        pass
