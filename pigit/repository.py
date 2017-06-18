from pigit.bean import GitObject
from pigit.bean.enum import SpecialReference
from pigit.configuration_provider import ConfigurationProvider
from pigit.dal import ObjectStore, ReferenceStore
from pigit.id_generator import IdGenerator
from pigit.working_area import WorkingArea


class Repository:
    def __init__(self, object_store: ObjectStore, reference_store: ReferenceStore, working_area: WorkingArea,
                 configuration_provider: ConfigurationProvider, id_generator: IdGenerator):
        self.object_store = object_store
        self.reference_store = reference_store
        self.configuration_provider = configuration_provider
        self.working_area = working_area
        self.id_generator = id_generator

    def log(self, params):
        pass

    def get_object(self, object_id) -> GitObject:
        return self.object_store.get_object(object_id)

    def get_head(self):
        return self.reference_store.get_special_ref(SpecialReference.HEAD)

    def checkout(self, branch):
        pass

    def stage_chunk(self, chunk):
        # TODO: Yet to figure out the details of this
        pass
