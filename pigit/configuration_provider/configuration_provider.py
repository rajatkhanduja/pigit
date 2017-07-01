from abc import ABCMeta, abstractmethod

from pathlib import Path


class ConfigurationProvider(metaclass=ABCMeta):
    def __init__(self, git_dir: Path):
        self.GIT_DIR = git_dir  # type: Path
        self.GIT_WORK_TREE = git_dir.parent
        self.GIT_OBJECT_DIRECTORY = git_dir / 'objects'


