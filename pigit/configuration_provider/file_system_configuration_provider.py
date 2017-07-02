from pathlib import Path

from .configuration_provider import ConfigurationProvider

import os


class FileSystemConfigurationProvider(ConfigurationProvider):
    def __init__(self, git_dir: Path, *, working_dir=None, object_dir=None):
        super().__init__(git_dir)

        self.env_props = {key: os.environ[key] for key in dir(self) if key.startswith('GIT_') and key in os.environ}
        self._update_properties_from_environment()

        if working_dir is not None:
            self.GIT_WORK_TREE = working_dir

        if object_dir is not None:
            self.GIT_OBJECT_DIRECTORY = object_dir

        self.GIT_IGNORE_FILE = self.GIT_WORK_TREE / '.gitignore'    # type: Path

        self.ignore_rules = self._get_gitignore_rules()

    def get_gitignore_rules(self):
        return self.ignore_rules

    def _update_properties_from_environment(self):
        for key in self.env_props:
            setattr(self, key, self.env_props[key])

    def _get_gitignore_rules(self):
        if not self.GIT_IGNORE_FILE.exists():
            return []

        rules = []

        with self.GIT_IGNORE_FILE.open() as ignore_file:
            for line in ignore_file:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue

                try:
                    end = line.index('#')
                    rules.append(line[:end])
                except ValueError:
                    rules.append(line)

        return rules
