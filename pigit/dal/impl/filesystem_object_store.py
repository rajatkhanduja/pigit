import os
import glob

from .default_serializer import DefaultSerializer
from .. import ObjectStore, SerializerDeserializer
from ...bean import GitObject
from ...exception import NotGitDirException, InvalidObjectNameException, DuplicateObjectException

OBJECT_ID_PREFIX_LEN = 2


def get_file_contents(file: str):
    with open(file, 'rb') as fp:
        return fp.read()


class FileSystemDataStore(ObjectStore):
    def __init__(self, working_dir, git_sub_directory: str = '.git',
                 serializer: SerializerDeserializer=DefaultSerializer()):
        self.working_dir = working_dir
        self.git_dir = os.path.join(working_dir, git_sub_directory)
        self.serializer = serializer
        if not os.path.isdir(self.git_dir):
            raise NotGitDirException(working_dir)

    def _get_base_object_dir(self):
        return os.path.join(self.git_dir, 'objects')

    def _get_obj_dir(self, object_id: str, make_dir: bool=False):
        if len(object_id) <= 2:
            raise InvalidObjectNameException(object_id)

        object_dir = os.path.join(self._get_base_object_dir(), object_id[:OBJECT_ID_PREFIX_LEN])
        if not os.path.isdir(object_dir):
            if make_dir:
                os.makedirs(object_dir)
            else:
                raise InvalidObjectNameException(object_id)
        return object_dir

    def _get_obj_file_path(self, object_id: str, make_dir: bool=False):
        object_dir = self._get_obj_dir(object_id, make_dir)
        return os.path.join(object_dir, object_id[OBJECT_ID_PREFIX_LEN:])

    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        object_file_pattern = self._get_obj_file_path(object_id) + "*"

        pattern_result = glob.glob(object_file_pattern)

        if len(pattern_result) != 1:
            raise InvalidObjectNameException(object_id)

        object_file = pattern_result[0]
        file_content = get_file_contents(object_file)
        git_object = self.serializer.deserialize(object_id, file_content)
        if not lazy_load:
            # TODO: Handle recursive loading
            pass
        return git_object

    def store_object(self, object: GitObject):
        object_file_path = self._get_obj_file_path(object.id, True)
        if os.path.isfile(object_file_path):
            raise DuplicateObjectException(object.id)
        with open(object_file_path, 'wb') as fp:
            fp.write(self.serializer.serialize(object))

    def delete_object(self, object_id):
        os.unlink(self._get_obj_file_path(object_id))
