from pathlib import Path

from pigit.configuration_provider import FileSystemConfigurationProvider
from pigit.store import FileSystemObjectStore, FileSystemReferenceStore
from pigit.id_generator import SerializerBasedIdGenerator
from pigit.serializer import DefaultSerializer
from pigit.working_area import FileSystemWorkingArea

from .repository import Repository
from .exception import *

from pigit.store import FileSystemReferenceStore, FileSystemObjectStore
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
    def repo(working_dir: str) -> Repository:
        working_dir_path = Path(working_dir)
        return Pigit.get_file_system_repository_from_directories(working_dir_path / '.git', working_dir_path)

    @staticmethod
    def get_file_system_repository_from_directories(git_dir: Path, working_dir: Path):
        serializer = DefaultSerializer()
        id_generator = SerializerBasedIdGenerator(serializer, sha1)
        configuration_provider = FileSystemConfigurationProvider(git_dir=git_dir)
        object_store = FileSystemObjectStore(objects_dir=configuration_provider.GIT_OBJECT_DIRECTORY,
                                             serializer=serializer)
        reference_store = FileSystemReferenceStore(configuration_provider.GIT_DIR)
        working_area = FileSystemWorkingArea(object_store, working_dir, configuration_provider.GIT_DIR)
        return Repository(object_store, reference_store, working_area, configuration_provider, id_generator)

