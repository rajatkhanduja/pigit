import zlib

from pathlib import Path
from pigit.store import ObjectStore
from pigit.serializer import Serializer
from pigit.bean import GitObject
from pigit.exception import InvalidObjectNameException, DuplicateObjectException, ObjectDirDoesNotExist

OBJECT_ID_PREFIX_LEN = 2


def get_file_contents(file: Path):
    with file.open(mode='rb') as fp:
        return fp.read()


class FileSystemObjectStore(ObjectStore):
    def __init__(self, serializer: Serializer, objects_dir: Path, initialize=False):
        self.serializer = serializer  # type: Serializer
        self.objects_dir = objects_dir

        if not initialize:
            if not self.objects_dir.exists():
                raise ObjectDirDoesNotExist(self.objects_dir)
        else:
            self.objects_dir.mkdir(exist_ok=True, parents=True)

    def _get_obj_dir(self, object_id: str, make_dir: bool = False) -> Path:
        if len(object_id) <= 2:
            raise InvalidObjectNameException(object_id)

        object_dir = self.objects_dir / object_id[:OBJECT_ID_PREFIX_LEN]
        if not object_dir.is_dir():
            if make_dir:
                object_dir.mkdir(parents=True, exist_ok=True)
            else:
                raise InvalidObjectNameException(object_id)
        return object_dir

    def _get_obj_file_path(self, object_id: str, make_dir: bool = False) -> Path:
        object_dir = self._get_obj_dir(object_id, make_dir)
        return object_dir / object_id[OBJECT_ID_PREFIX_LEN:]

    def get_object(self, object_id: str, lazy_load=True) -> GitObject:
        pattern_result = list(self._get_obj_dir(object_id).glob(object_id[OBJECT_ID_PREFIX_LEN:] + "*"))

        if len(pattern_result) != 1:
            raise InvalidObjectNameException(object_id)

        object_file = pattern_result[0]
        if not object_file.is_file():
            raise InvalidObjectNameException(object_id)
        file_content = get_file_contents(object_file)
        decomressed_content = zlib.decompress(file_content)
        git_object = self.serializer.deserialize(object_id, decomressed_content)

        if not lazy_load:
            # TODO: Handle recursive loading
            pass
        return git_object

    def store_object(self, object: GitObject):
        object_file_path = self._get_obj_file_path(object.id, True)
        if object_file_path.is_file():
            raise DuplicateObjectException(object.id)
        with object_file_path.open('wb') as fp:
            serilized_bytes = self.serializer.serialize(object)
            fp.write(zlib.compress(serilized_bytes))

    def delete_object(self, object_id):
        self._get_obj_file_path(object_id).unlink()

