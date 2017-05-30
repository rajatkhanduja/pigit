from .repository import Repository
from .exception import *
from .dal import FileSystemDataStore


class PigitCommandWrapper:
    def __init__(self, dir: str):
        self.dir = dir
        data_store = FileSystemDataStore(dir)
        reference_store = None
        working_area = None
        configuration_provider = None
        self.repository = Repository(data_store, reference_store, working_area, configuration_provider)

    def execute_command(self, command_params):
        try:
            print(self.repository.get_object(command_params[1]))
        except PigitException as e:
            print(e.message)
