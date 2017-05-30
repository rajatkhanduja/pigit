from abc import ABCMeta, abstractmethod


class ConfigurationProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_property(self, key) -> str:
        pass
