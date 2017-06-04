from abc import ABCMeta, abstractmethod
from ..bean import Reference
from ..bean.enum import SpecialReference


class ReferenceStore(metaclass=ABCMeta):
    def get_special_ref(self, special_ref: SpecialReference) -> Reference:
        """
        :param special_ref: One of the SpecialReference enum values
        :raises: NoSuchSpecialReferenceException, NoSuchReferenceException
        :return: Reference
        """
        reference = self.resolve_special_ref(special_ref)
        return self.get_reference(reference)

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
    def get_reference(self, reference: str) -> Reference:
        """
        Method to get a `Reference` object from reference string
        :param reference: str , reference identifier
        :raises: NoSuchReferenceException
        :return: Reference
        """
        pass

    @abstractmethod
    def store_reference(self, reference: Reference):
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
    def get_all_branches(self, include_remote=False) -> [Reference]:
        """
        Method to get a list of all branches
        :return: [Reference]
        """
        pass
