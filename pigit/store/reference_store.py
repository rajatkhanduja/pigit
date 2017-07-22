from abc import ABCMeta, abstractmethod
from typing import Generator

from pigit.exception import BranchNameNotRecognizedException, NoSuchReferenceException, SpecialReferenceNotSetException
from pigit.bean import Reference, Index
from pigit.bean.enum import SpecialReference


class ReferenceStore(metaclass=ABCMeta):
    def get_special_ref(self, special_ref: SpecialReference) -> Reference:
        """
        :param special_ref: One of the SpecialReference enum values
        :raises: NoSuchSpecialReferenceException, NoSuchReferenceException
        :return: Reference
        """
        reference = self.resolve_special_ref(special_ref)
        try:
            return self._get_reference_by_relative_path(reference)
        except NoSuchReferenceException:
            return Reference(reference, None)

    @abstractmethod
    def resolve_special_ref(self, special_ref: SpecialReference) -> str:
        """
        Method to resolve a special reference to a regular reference string
        :param special_ref:
        :raises: NoSuchSpecialReferenceException
        :return: str
        """
        pass

    @abstractmethod
    def _get_reference_by_relative_path(self, reference_path: str) -> Reference:
        pass

    @abstractmethod
    def get_reference(self, reference: str) -> Reference:
        """
        Method to get a `Reference` object from reference string
        :param reference: str , reference identifier
        :raises: NoSuchReferenceException
        :return: Reference
        """
        pass

    @abstractmethod
    def store_reference(self, reference: Reference, update: bool=False):
        pass

    @abstractmethod
    def get_symbolic_ref(self, reference_id) -> str:
        pass

    @abstractmethod
    def get_branch(self, branch_name: str) -> Reference:
        """
        Method to get a `Reference` object from branch name
        :param branch_name:
        :raises: NoSuchBranchException
        :return: Reference
        """
        pass

    @abstractmethod
    def remove_branch(self, branch_name: str):
        """
        Method to remove branch
        :param branch_name:
        :raises: NoSuchBranchException
        :return: 
        """
        pass

    @abstractmethod
    def get_all_branches(self, include_remote=False) -> Generator[Reference, None, None]:
        """
        Method to get a list of all branches
        :return: Generator[Reference, None, None]
        """
        pass

    @abstractmethod
    def get_references(self) -> Generator[Reference, None, None]:
        """
        Method to get all references
        :return: 
        """
        pass

    @property
    def branches(self):
        return self.get_all_branches()

    def get_branch_name(self, reference: Reference, local=True) -> str:
        """
        Method to get branch name from the reference name. For instance '/refs/heads/master' resolves to 'master'
        and '/refs/remotes/origin/master' resovles to '/remotes/origin/master'
        :param reference: 
        :param local: 
        :return: 
        """
        ref_name = reference.name
        search_string = '/heads/' if local else '/remotes/'
        try:
            return ref_name[ref_name.index(search_string) + len(search_string):]
        except (ValueError, IndexError):
            raise BranchNameNotRecognizedException(ref_name)

    @abstractmethod
    def remove_reference(self, reference_name: str):
        pass
