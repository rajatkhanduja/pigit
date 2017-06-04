from .repository_factory import RepositoryFactory
from .exception import *


class PigitCommandWrapper:
    def __init__(self, directory: str):
        self.dir = directory
        self.repository = RepositoryFactory.get_repository_from_working_dir(directory)

    def execute_command(self, command_params):
        try:
            print(self.repository.get_object(command_params[1]))
        except PigitException as e:
            print(e.message)
