import os

from .default_serializer import DefaultSerializer
from .. import ObjectStore
from ...bean import GitObject, Commit
from ...exception import NotGitDirException, ObjectNotFoundException


def get_file_contents(file: str):
    with open(file, 'rb') as fp:
        return fp.read()


class FileSystemDataStore(ObjectStore):
    def __init__(self, working_dir, serializer=DefaultSerializer()):
        self.working_dir = working_dir
        self.git_dir = os.path.join(working_dir, '.git')
        self.serializer = serializer
        if not os.path.isdir(self.git_dir):
            raise NotGitDirException(working_dir)

    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        prefix, tail = object_id[:2], object_id[2:]
        object_file = os.path.join(self.git_dir, 'objects', prefix, tail)
        if not os.path.isfile(object_file):
            raise ObjectNotFoundException(object_id)

        file_content = get_file_contents(object_file)
        git_object = self.serializer.deserialize(object_id, file_content)
        if not lazy_load:
            #TODO: Handle recursive loading
            pass
        return git_object

    def store_object(self, object: GitObject):
        raise NotImplementedError("Not yet implemented")

    def get_commit(self, commit_id) -> Commit:
        pass

    def get_snapshot(self, tree_reference):
        pass
