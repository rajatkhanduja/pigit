from .dal import ObjectStore, ReferenceStore
from .configuration_provider import ConfigurationProvider
from .working_area import WorkingArea
from .bean import GitObject


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
        return self.reference_store.get_head()

    def checkout(self, branch, new_branch=False, detach=False):
        if not new_branch:
            commit_id = self.reference_store.get_reference(branch)
            commit = self.object_store.get_commit(commit_id)
            tree = self.object_store.get_snapshot(commit.tree_reference)
            self.working_area.setup(tree)
        else:
            self.reference_store.create_reference(branch, self.get_head())
            self.reference_store.update_current_branch()

    def stage_chunk(self, chunk):
        # TODO: Yet to figure out the details of this
        pass
