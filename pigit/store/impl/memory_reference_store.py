from typing import Dict, Generator

from pigit.bean import Reference, Index
from pigit.bean.enum import SpecialReference
from pigit.store import ReferenceStore
from pigit.exception import NoSuchSpecialReferenceException, IndexNotFoundException, BranchNameNotRecognizedException, \
    NoSuchReferenceException, ReferenceAlreadyExistsException


class MemoryReferenceStore(ReferenceStore):
    def __init__(self):
        self.references = {}            # type: Dict[str, Reference]
        self.special_references = {}    # type: Dict[SpecialReference, str]
        self.index = None               # type: Index
        self.branch2ref = {}              # type: Dict[str, Reference]
        self.tags = {}

        self.special_references[SpecialReference.HEAD] = "refs/heads/master"

    def resolve_special_ref(self, special_ref: SpecialReference) -> str:
        if special_ref in self.special_references:
            return self.special_references[special_ref]
        raise NoSuchSpecialReferenceException()

    def get_references(self) -> Generator[Reference, None, None]:
        for reference in self.references:
            yield reference

    def get_all_branches(self, include_remote=False) -> [Reference]:
        return [self.branches[branch] for branch in self.branch2ref]

    def store_reference(self, reference: Reference, update: bool=False):
        if reference.name not in self.references or update:
            self.references[reference.name] = reference
        else:
            raise ReferenceAlreadyExistsException(reference.name)

    def get_reference(self, reference: str) -> Reference:
        return self._get_reference_by_relative_path(reference)

    def remove_branch(self, branch_name: str):
        if branch_name not in self.branches:
            raise BranchNameNotRecognizedException(branch_name)

        del self.branches[branch_name]

    def get_symbolic_ref(self, reference_id) -> str:
        pass

    def _get_reference_by_relative_path(self, reference_path: str) -> Reference:
        try:
            return self.references[reference_path]
        except KeyError:
            raise NoSuchReferenceException(reference_path)

    def get_branch(self, branch_name: str) -> Reference:
        try:
            return self.branches[branch_name]
        except KeyError:
            raise BranchNameNotRecognizedException(branch_name)

    def get_index(self) -> Index:
        if self.index is None:
            raise IndexNotFoundException
        return self.index

    def remove_reference(self, reference_name: str):
        if reference_name in self.references:
            del self.references[reference_name]

    @classmethod
    def from_reference_store(cls, reference_store: ReferenceStore):
        store = MemoryReferenceStore()

        for reference in reference_store.get_references():
            store.store_reference(reference)

        for reference in reference_store.branches:
            store.branch2ref[reference.name] = reference

        return store
