from pathlib import Path
from typing import Generator

from pigit.bean import GitObject, Tree, Commit, IndexEntry, Blob
from pigit.bean.enum import SpecialReference
from pigit.configuration_provider import ConfigurationProvider
from pigit.store import ObjectStore, ReferenceStore
from pigit.id_generator import IdGenerator
from pigit.working_area import WorkingArea
from pigit.exception import IndexNotFoundException


class Repository:
    def __init__(self, object_store: ObjectStore, reference_store: ReferenceStore, working_area: WorkingArea,
                 configuration_provider: ConfigurationProvider, id_generator: IdGenerator):
        self.object_store = object_store
        self.reference_store = reference_store
        self.configuration_provider = configuration_provider
        self.working_area = working_area
        self.id_generator = id_generator

    def get_logs(self, *, last_commit=None) -> Generator[Commit, None, None]:
        if last_commit is None:
            last_commit = self.get_head().commit

        # TODO: Make this part correctly traverse for merges and multiple parents scenario
        commit = self.object_store.get_object(last_commit)  # type: Commit
        while commit is not None:
            yield commit
            if commit.parents is None or len(commit.parents) == 0:
                break
            commit = self.object_store.get_object(commit.parents[0].id)

    def get_object(self, object_id) -> GitObject:
        return self.object_store.get_object(object_id)

    def get_head(self):
        return self.reference_store.get_special_ref(SpecialReference.HEAD)

    def checkout(self, branch):
        branch_reference = self.reference_store.get_branch(branch)
        commit = self.object_store.get_object(branch_reference.commit)  # type: Commit
        snapshot = self.object_store.get_object(commit.tree.id)  # type: Tree
        self.working_area.setup(snapshot)

    def get_branches(self, include_remote=False):
        return self.reference_store.get_all_branches(include_remote=include_remote)

    def stage_chunk(self, chunk):
        # TODO: Yet to figure out the details of this
        pass

    def get_index(self):
        return self.reference_store.get_index()

    @property
    def head(self):
        return self.get_head()

    @property
    def log(self):
        return self.get_logs()

    @property
    def branches(self):
        return self.get_branches(include_remote=True)

    @property
    def index(self):
        return self.get_index()

    def create_branch(self, branch_name: str):
        pass

    def has_changed(self, entry: IndexEntry):
        blob = Blob(None, self.working_area.get_file_content(entry.path))
        return self.id_generator.generate_id(blob) != entry.sha1

    def get_status(self):
        index = self.index

        changed = set()
        created = set()

        index_entries_by_path = {entry.path: entry for entry in index.entries}

        files_in_working_area = set(self.working_area.get_files())
        for file in files_in_working_area:
            if file not in index_entries_by_path:
                created.add(file)
            else:
                entry = index_entries_by_path[file]     # type: IndexEntry
                if self.has_changed(entry):
                    changed.add(file)

        deleted = set(file for file in index_entries_by_path if file not in files_in_working_area)

        return changed, created, deleted

