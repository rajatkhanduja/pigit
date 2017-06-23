from pathlib import Path

from .configuration_provider import ConfigurationProvider

import os


class FileSystemConfigurationProvider(ConfigurationProvider):
    def get_property(self, key) -> str:
        pass

    def __init__(self, *, git_dir: Path, working_dir=None):
        self.properties = {
            'GIT_DIR': git_dir,
            'GIT_WORK_TREE ': git_dir.parent,
            'GIT_OBJECT_DIRECTORY': git_dir / '.objects'
        }


