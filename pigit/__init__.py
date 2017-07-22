from pathlib import Path
from hashlib import sha1

from pigit.configuration_provider import FileSystemConfigurationProvider
from pigit.staging_area import FileSystemStagingArea
from pigit.staging_area.memory_staging_area import MemoryStagingArea
from pigit.store import FileSystemObjectStore, FileSystemReferenceStore
from pigit.store import MemoryObjectStore, MemoryReferenceStore
from pigit.id_generator import SerializerBasedIdGenerator
from pigit.serializer import DefaultSerializer
from pigit.working_area import FileSystemWorkingArea, MemoryWorkingArea

from .repository import Repository
from .exception import *


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
        working_area = FileSystemWorkingArea(object_store, working_dir, configuration_provider.GIT_DIR, configuration_provider.get_gitignore_rules())
        staging_area = FileSystemStagingArea(git_dir=configuration_provider.GIT_DIR)
        return Repository(object_store, reference_store, working_area, configuration_provider, id_generator, staging_area)

    @staticmethod
    def get_memory_repository():
        serializer = DefaultSerializer()
        id_generator = SerializerBasedIdGenerator(serializer, sha1)
        configuration_provider = FileSystemConfigurationProvider(Path('.git'))
        object_store = MemoryObjectStore()
        reference_store = MemoryReferenceStore()
        working_area = MemoryWorkingArea(object_store, configuration_provider.GIT_WORK_TREE)
        staging_area = MemoryStagingArea(configuration_provider.GIT_WORK_TREE)

        return Repository(object_store, reference_store, working_area, configuration_provider, id_generator,
                          staging_area)

    @staticmethod
    def get_memory_repository_from_repository(repo: Repository):
        object_store = MemoryObjectStore.from_object_store(repo.object_store)
        reference_store = MemoryReferenceStore.from_reference_store(repo.reference_store)

        pass

