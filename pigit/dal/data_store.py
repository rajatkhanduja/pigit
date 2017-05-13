from abc import ABCMeta, abstractmethod


class DataStore(metaclass=ABCMeta):

    @abstractmethod
    def get_object(self, object_id):
        pass