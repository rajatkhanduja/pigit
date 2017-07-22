# IndexEntry = collections.namedtuple('IndexEntry', [
#     'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode',
#     'uid', 'gid', 'size', 'sha1', 'flags', 'path',
# ])
from pathlib import Path
from typing import List


def get_file_mode_for_index(file: Path):
    return file.stat().st_mode

class IndexEntry(object):
    def __init__(self, ctime_s: int, ctime_n: int, mtime_s: int, mtime_n: int, dev, ino, mode, uid, gid, size,
                 sha1: str,
                 flags, path: str):
        self.ctime_s = ctime_s
        self.ctime_n = ctime_n
        self.mtime_s = mtime_s
        self.mtime_n = mtime_n
        self.dev = dev
        self.ino = ino
        self.mode = mode
        self.uid = uid
        self.gid = gid
        self.size = size
        self.sha1 = sha1
        self.flags = flags
        self.path = path

    def __repr__(self):
        return repr(self.__dict__)

    @classmethod
    def from_file(cls, file: Path, sha1, relative_path: str):
        fstat = file.stat()
        mode = get_file_mode_for_index(file)

        return IndexEntry(fstat.st_ctime, fstat.st_ctime_ns, fstat.st_mtime, fstat.st_mtime_ns, fstat.st_dev,
                          fstat.st_ino, mode, fstat.st_uid, fstat.st_gid, fstat.st_size, sha1, fstat.st_flags,
                          relative_path)


class Index(object):
    def __init__(self, signature: str, version: int):
        self.signature = signature
        self.version = version
        self.entries = []   # type: List[IndexEntry]

    def add_index_entry(self, entry: IndexEntry):
        self.entries.append(entry)

    def __repr__(self):
        return repr(self.__dict__)
