from pathlib import Path

from .configuration_provider import ConfigurationProvider

import os


class FileSystemConfigurationProvider(ConfigurationProvider):
    def get_property(self, key):
        pass

    def _update_properties_from_environment(self):
        for key in self.env_props:
            setattr(self, key, self.env_props[key])

    def __init__(self, git_dir: Path, *, working_dir=None, object_dir=None):
        super().__init__(git_dir)

        self.env_props = {key: os.environ[key] for key in dir(self) if key.startswith('GIT_') and key in os.environ}
        self._update_properties_from_environment()

        if working_dir is not None:
            self.GIT_WORK_TREE = working_dir

        if object_dir is not None:
            self.GIT_OBJECT_DIRECTORY = object_dir



