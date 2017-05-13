import os

import zlib

from ..bean.enum import GitObjectType
from ..bean import GitObject, TreeObject, CommitObject, BlobObject
from ..exception import NotGitDirException, ObjectNotFoundException
from .data_store import DataStore


def get_uncompressed_file_content(file: str) -> bytes:
    with open(file, 'rb') as fp:
        return zlib.decompress(fp.read())


def get_header_content(file_content: bytes) -> (str, str):
    header_bytes, content_bytes = file_content.split(b'\x00')
    header = header_bytes.decode("utf-8")
    content = content_bytes.decode("utf-8")
    return header, content


def infer_type_and_length(header) -> (GitObjectType, int):
    object_type = None
    length = 0
    if header.startswith('blob'):
        object_type = GitObjectType.BLOB
        length = int(header[4:].strip())
    elif header.startswith('commit'):
        object_type = GitObjectType.COMMIT
        length = int(header[6:].strip())
    elif header.startswith('tree'):
        object_type = GitObjectType.TREE
        length = int(header[4:].strip())

    return object_type, length


class FileSystemDataStore(DataStore):
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.git_dir = os.path.join(working_dir, '.git')
        if not os.path.isdir(self.git_dir):
            raise NotGitDirException(working_dir)

    def get_object(self, object_id):
        prefix, tail = object_id[:2], object_id[2:]
        object_file = os.path.join(self.git_dir, 'objects', prefix, tail)
        if not os.path.isfile(object_file):
            raise ObjectNotFoundException(object_id)

        file_content = get_uncompressed_file_content(object_file)
        header, content = get_header_content(file_content)
        object_type, length = infer_type_and_length(header)

        if object_type == GitObjectType.BLOB:
            return BlobObject(object_id, content)
        elif object_type == GitObjectType.COMMIT:
            return CommitObject(object_id, content)
        elif object_type == GitObjectType.TREE:
            return TreeObject(object_id, content)
