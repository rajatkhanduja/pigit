
from .dal import DataStore
from .bean import GitObject


class Pigit:
    def __init__(self, data_store: DataStore, conf: dict):
        self.data_store = data_store

    def log(self, params):
        pass

    def get_object(self, object_id) -> GitObject:
        return self.data_store.get_object(object_id)

    def cat_file(self, object_id):
        obj = self.get_object(object_id)
        return obj.id, obj.content

    @classmethod
    def find_git_dir(cls, cur_dir):
        pass
