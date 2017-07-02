import hashlib
import struct
from pathlib import Path
from typing import Generator, List

import binascii

from pigit.store.reference_store import ReferenceStore
from pigit.exception import NoSuchReferenceException, IndexNotFoundException, IndexCorruptedException, \
    IndexChecksumDoesNotMatchException, BranchNameNotRecognizedException
from pigit.bean import Reference, Index, IndexEntry
from pigit.bean.enum import SpecialReference

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


class FileSystemReferenceStore(ReferenceStore):
    def __init__(self, git_dir: Path, *, refs_sub_directory: str = 'refs', local_branches_sub_dir='heads',
                 remote_branches_sub_dir='remotes'):

        self.git_dir = git_dir

        self.ref_dir = self.git_dir / refs_sub_directory
        self.ref_dir.mkdir(exist_ok=True)

        self.local_branches_dir = self.ref_dir / local_branches_sub_dir
        self.local_branches_dir.mkdir(exist_ok=True)

        self.remote_branches_sub_dir = self.ref_dir / remote_branches_sub_dir
        self.remote_branches_sub_dir.mkdir(exist_ok=True)

        self.index_file = self.git_dir / 'index'

    def get_all_branches(self, include_remote=False) -> Generator[Reference, None, None]:
        for path in self.local_branches_dir.glob("*"):  # type: Path
            commit_id = path.open().read().strip()
            branch_name = str(path.relative_to(self.local_branches_dir))
            yield Reference(branch_name, commit_id)

        if include_remote:
            for path in self.remote_branches_sub_dir.rglob("*"):
                if path.is_file():
                    commit_id = path.open().read().strip()
                    branch_name = "remotes/" + str(path.relative_to(self.remote_branches_sub_dir))
                    yield Reference(branch_name, commit_id)

    def get_branch(self, branch_name: str) -> Reference:
        if len(branch_name.split('/')) > 1:
            # Assume it to be a remote branch
            branch_name = "remotes/" + branch_name
        reference = "heads/" + branch_name
        return self.get_reference(reference)

    def remove_branch(self, branch_name: str):
        pass

    def resolve_special_ref(self, special_ref: SpecialReference) -> str:
        file_path = self.git_dir / special_ref.value
        try:
            content = file_path.open().read().strip()
            if content.startswith('ref: '):
                return content[5:]
        except FileNotFoundError:
            raise NoSuchReferenceException(special_ref.value)

    def store_reference(self, reference: Reference):
        raise NotImplementedError

    def get_reference(self, reference: str) -> Reference:
        reference_file = self.ref_dir / reference
        if not reference_file.is_file():
            raise NoSuchReferenceException(reference)
        commit_id = reference_file.open().read().strip()
        return Reference(reference, commit_id)

    def get_symbolic_ref(self, reference_id: str) -> str:
        pass

    def get_reference_by_relative_path(self, reference_path: str):
        reference_file = self.git_dir / reference_path
        if not reference_file.is_file():
            raise NoSuchReferenceException(reference_path)
        commit_id = reference_file.open().read().strip()
        return Reference(reference_path, commit_id)

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

    def get_branch_name(self, reference: Reference, local=True) -> str:
        ref_name = reference.name
        search_string = '/heads/' if local else '/remotes/'
        try:
            return ref_name[ref_name.index(search_string) + len(search_string):]
        except (ValueError, IndexError):
            raise BranchNameNotRecognizedException(ref_name)
