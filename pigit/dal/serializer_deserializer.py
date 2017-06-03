from abc import ABCMeta, abstractmethod

from ..bean import GitObject


class SerializerDeserializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, object: GitObject) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, object_id: str, serialized_bytes: bytes) -> GitObject:
        pass
