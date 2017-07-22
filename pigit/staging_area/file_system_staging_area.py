import hashlib
import struct
import binascii

from pathlib import Path
from typing import Generator

from pigit.exception import IndexNotFoundException, IndexCorruptedException, IndexChecksumDoesNotMatchException
from pigit.bean import Index, IndexEntry
from .staging_area import StagingArea

INDEX_ENTRY_BYTES = 62


def get_index_entries(entry_data: bytes, num_entries):
    start = 0

    def get_index_entry_data_chunks(entry_data: bytes, num_entries: int) -> Generator[bytes, None, None]:
        nonlocal start

        while start + INDEX_ENTRY_BYTES < len(entry_data) and num_entries > 0:
            end = entry_data.index(b'\x00', start + INDEX_ENTRY_BYTES)
            yield entry_data[start: end]
            num_entries -= 1
            start += (((end - start) + 8) // 8) * 8

    def get_index_entry(entry_data_chunk):
        ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags = \
            struct.unpack('!LLLLLLLLLL20sH', entry_data_chunk[:INDEX_ENTRY_BYTES])

        sha1 = binascii.hexlify(sha1).decode()
        path = entry_data_chunk[INDEX_ENTRY_BYTES:].decode()

        return IndexEntry(ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, path)

    return [get_index_entry(entry_data_chunk) for entry_data_chunk in
            get_index_entry_data_chunks(entry_data, num_entries)], start


class FileSystemStagingArea(StagingArea):
    def __init__(self, git_dir: Path):
        self.git_dir = git_dir
        self.index_file = self.git_dir / 'index'

    def get_index(self) -> Index:
        # Inspired from http://benhoyt.com/writings/pygit/
        #
        # Technical documentation at
        # https://github.com/git/git/blob/867b1c1bf68363bcfd17667d6d4b9031fa6a1300/Documentation/technical/index-format.txt#L38

        try:
            with self.index_file.open('rb') as fp:
                index_content = fp.read()
        except FileNotFoundError:
            raise IndexNotFoundException
        except IOError:
            raise IndexCorruptedException

        digest = hashlib.sha1(index_content[:-20]).digest()
        if digest != index_content[-20:]:
            raise IndexChecksumDoesNotMatchException(index_content[-20:], digest)

        try:
            signature, version, num_entries = struct.unpack('!4sLL', index_content[:12])
            index = Index(signature, version)

            entry_data = index_content[12:-20]
            index.entries, content_idx = get_index_entries(entry_data, num_entries)
            if content_idx < len(entry_data):
                # TODO: Parse for extensions
                pass

            return index
        except:
            raise IndexCorruptedException
