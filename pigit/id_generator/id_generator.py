from abc import ABCMeta
from ..bean import GitObject


class IdGenerator(metaclass=ABCMeta):
    def generate_id(self, git_object: GitObject) -> str:
        pass
