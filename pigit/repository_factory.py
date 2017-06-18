from .dal import FileSystemReferenceStore, FileSystemObjectStore
from .repository import Repository


class RepositoryFactory(object):
    @staticmethod
    def get_repository_from_working_dir(working_dir: str) -> Repository:
        object_store = FileSystemObjectStore(working_dir)
        reference_store = FileSystemReferenceStore(working_dir)
        working_area = None
        configuration_provider = None
        return Repository(object_store, reference_store, working_area, configuration_provider)
