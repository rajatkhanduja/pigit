from abc import ABCMeta, abstractmethod


class ReferenceStore(metaclass=ABCMeta):
    @abstractmethod
    def get_reference(self, reference_id):
        pass

    @abstractmethod
    def get_head(self) -> str:
        pass

    @abstractmethod
    def create_reference(self, name, commit_id):
        pass


