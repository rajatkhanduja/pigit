from ..serializer_deserializer import SerializerDeserializer
from ..id_generator import IdGenerator
from ...bean import GitObject


class SerializerBasedIdGenerator(IdGenerator):
    def __init__(self, serializer: SerializerDeserializer, hasher):
        self.serializer = serializer
        self.hasher = hasher

    def generate_id(self, git_object: GitObject) -> str:
        serialized_bytes = self.serializer.serialize(git_object)
        return self.hasher(serialized_bytes).hexdigest()
