from typing import Set


class RepositoryStatus(object):

    def __init__(self, branch_name: str, created: Set[str], changed: Set[str], deleted: Set[str]):
        self.branch_name = branch_name
        self.created = created
        self.changed = changed
        self.deleted = deleted

    def __repr__(self):
        return repr(self.__dict__)
