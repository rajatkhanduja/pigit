import os
from pathlib import Path
from typing import Generator

from pigit.store.reference_store import ReferenceStore
from pigit.exception import NotGitDirException, NoSuchReferenceException
from pigit.bean import Reference
from pigit.bean.enum import SpecialReference


class FileSystemReferenceStore(ReferenceStore):
    def __init__(self, git_dir: Path, refs_sub_directory: str = 'refs', local_branches_sub_dir='heads',
                 remote_branches_sub_dir='remotes'):

        self.git_dir = git_dir

        self.ref_dir = self.git_dir / refs_sub_directory
        self.ref_dir.mkdir(exist_ok=True)

        self.local_branches_dir = self.ref_dir / local_branches_sub_dir
        self.local_branches_dir.mkdir(exist_ok=True)

        self.remote_branches_sub_dir = self.ref_dir / remote_branches_sub_dir
        self.remote_branches_sub_dir.mkdir(exist_ok=True)

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