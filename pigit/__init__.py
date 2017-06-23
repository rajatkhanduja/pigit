from pigit.dal import FileSystemObjectStore, FileSystemReferenceStore
from pigit.id_generator import SerializerBasedIdGenerator
from pigit.serializer import DefaultSerializer
from pigit.working_area import FileSystemWorkingArea

from .repository import Repository
from .exception import *

from pigit.dal import FileSystemReferenceStore, FileSystemObjectStore
from pigit.working_area import FileSystemWorkingArea
from pigit.serializer import DefaultSerializer
from pigit.id_generator import SerializerBasedIdGenerator
from pigit.repository import Repository
from hashlib import sha1


class Pigit(object):
    @staticmethod
    def init(working_dir):
        pass

    @staticmethod
    def get_repository_from_working_dir(working_dir: str) -> Repository:
        return Pigit.get_file_system_repository_from_directories(working_dir, working_dir)

    @staticmethod
    def get_file_system_repository_from_directories(git_parent_dir: str, working_dir: str):
        serializer = DefaultSerializer()
        id_generator = SerializerBasedIdGenerator(serializer, sha1)
        object_store = FileSystemObjectStore(git_parent_dir, serializer=serializer)
        reference_store = FileSystemReferenceStore(git_parent_dir)
        working_area = FileSystemWorkingArea(object_store, working_dir)
        configuration_provider = None
        return Repository(object_store, reference_store, working_area, configuration_provider, id_generator)


class PigitCommandWrapper:
    def __init__(self, directory: str):
        self.dir = directory
        self.repository = Pigit.get_repository_from_working_dir(directory)

    def execute_command(self, command_params):
        try:
            print(self.repository.get_object(command_params[1]))
        except PigitException as e:
            print(e.message)
