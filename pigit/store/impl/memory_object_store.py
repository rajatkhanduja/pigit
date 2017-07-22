from typing import Dict

from pigit.exception import InvalidObjectNameException, DuplicateObjectException
from pigit.bean import GitObject
from pigit.store import ObjectStore


class MemoryObjectStore(ObjectStore):
    def __init__(self):
        self.objects = {}   # type: Dict[str, GitObject]

    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        try:
            return self.objects[object_id]
        except KeyError:
            raise InvalidObjectNameException(object_id)

    def store_object(self, object: GitObject):
        assert object.id is not None

        if object.id in self.objects:
            raise DuplicateObjectException(object.id)

        self.objects[object.id] = object

    def get_all_objects(self):
        for object_id in self.objects:
            yield self.objects[object_id]

    def delete_object(self, object_id: str):
        if object_id in self.objects:
            del self.objects[object_id]

    @classmethod
    def from_object_store(cls, object_store: ObjectStore) -> 'MemoryObjectStore':
        store = MemoryObjectStore()

        for git_object in object_store.get_all_objects():
            store.store_object(git_object)

        return store
