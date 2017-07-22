from typing import Union


class Reference(object):
    def __init__(self, name: str, commit_id: Union[str, None]):
        self.name = name
        self.commit = commit_id
