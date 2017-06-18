from pigit.dal import FileSystemReferenceStore, FileSystemObjectStore, DefaultSerializer
from pigit.id_generator import SerializerBasedIdGenerator
from pigit.repository import Repository
from hashlib import sha1


class RepositoryFactory(object):
    @staticmethod
    def get_repository_from_working_dir(working_dir: str) -> Repository:
        serializer = DefaultSerializer()
        id_generator = SerializerBasedIdGenerator(serializer, sha1)
        object_store = FileSystemObjectStore(working_dir, serializer=serializer)
        reference_store = FileSystemReferenceStore(working_dir)
        working_area = None
        configuration_provider = None
        return Repository(object_store, reference_store, working_area, configuration_provider, id_generator)
