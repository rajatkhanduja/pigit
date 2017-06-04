import os

from ..reference_store import ReferenceStore
from ...exception import NotGitDirException, NoSuchReferenceException
from ...bean import Reference
from ...bean.enum import SpecialReference


class FileSystemReferenceStore(ReferenceStore):
    def get_all_branches(self, include_remote=False) -> [Reference]:
        pass

    def get_branch(self, branch_name: str) -> Reference:
        if len(branch_name.split('/')) > 1:
            # Assume it to be a remote branch
            branch_name = "remotes/" + branch_name
        reference = "heads/" + branch_name
        return self.get_reference(reference)

    def remove_branch(self, branch_name: str):
        pass

    def __init__(self, working_dir, git_sub_directory: str = '.git', refs_sub_directory: str = 'refs'):
        self.working_dir = working_dir
        self.git_dir = os.path.join(working_dir, git_sub_directory)
        if not os.path.isdir(self.git_dir):
            raise NotGitDirException(working_dir)

        self.ref_dir = os.path.join(self.git_dir, refs_sub_directory)

    def resolve_special_ref(self, special_ref: SpecialReference) -> str:
        file_path = os.path.join(self.ref_dir, special_ref.value)
        try:
            content = open(file_path).read().strip()
            if content.startswith('ref: '):
                return content[5:]
        except FileNotFoundError:
            pass

    def store_reference(self, reference: Reference):
        raise NotImplementedError

    def get_reference(self, reference: str) -> Reference:
        parts = reference.split('/')
        reference_file = os.path.join(self.ref_dir, *parts)
        if not os.path.isfile(reference_file):
            raise NoSuchReferenceException(reference)
        commit_id = open(reference_file).read().strip()
        return Reference(reference, commit_id)

    def get_symbolic_ref(self, reference_id: str) -> str:
        pass
