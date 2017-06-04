from .bean import GitObject
from .bean.enum import SpecialReference
from .configuration_provider import ConfigurationProvider
from .dal import ObjectStore, ReferenceStore
from .working_area import WorkingArea


class Repository:
    def __init__(self, object_store: ObjectStore, reference_store: ReferenceStore, working_area: WorkingArea,
                 configuration_provider: ConfigurationProvider):
        self.object_store = object_store
        self.reference_store = reference_store
        self.configuration_provider = configuration_provider
        self.working_area = working_area

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
