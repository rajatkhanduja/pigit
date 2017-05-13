from .pigit import Pigit
from .exception import *
from .dal import FileSystemDataStore

class PigitCommandWrapper:
    def __init__(self, dir: str):
        self.dir = dir
        data_store = FileSystemDataStore(dir)
        self.pigit = Pigit(data_store, {})

    def execute_command(self, command_params):
        try:
            print(self.pigit.cat_file(command_params[1]))
        except PigitException as e:
            print(e.message)
