from pigit.dal import FileSystemReferenceStore, FileSystemObjectStore
from pigit.working_area import FileSystemWorkingArea
from pigit.serializer import DefaultSerializer
from pigit.id_generator import SerializerBasedIdGenerator
from pigit.repository import Repository
from hashlib import sha1


class RepositoryFactory(object):
    @staticmethod
    def get_repository_from_working_dir(working_dir: str) -> Repository:
        return RepositoryFactory.get_file_system_repository_from_directories(working_dir, working_dir)

    @staticmethod
    def get_file_system_repository_from_directories(git_parent_dir: str, working_dir: str):
        serializer = DefaultSerializer()
        id_generator = SerializerBasedIdGenerator(serializer, sha1)
        object_store = FileSystemObjectStore(git_parent_dir, serializer=serializer)
        reference_store = FileSystemReferenceStore(git_parent_dir)
        working_area = FileSystemWorkingArea(object_store, working_dir)
        configuration_provider = None
        return Repository(object_store, reference_store, working_area, configuration_provider, id_generator)