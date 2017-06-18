from pigit.bean import GitObject
from pigit.id_generator.id_generator import IdGenerator
from pigit.serializer.serializer import Serializer


class SerializerBasedIdGenerator(IdGenerator):
    def __init__(self, serializer: Serializer, hasher):
        self.serializer = serializer
        self.hasher = hasher

    def generate_id(self, git_object: GitObject) -> str:
        serialized_bytes = self.serializer.serialize(git_object)
        return self.hasher(serialized_bytes).hexdigest()
