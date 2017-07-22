from pathlib import Path
from typing import Generator, List, Tuple

from pigit.exception import DuplicateObjectException, NothingToCommitException, SpecialReferenceNotSetException, \
    IndexNotFoundException
from pigit.bean import GitObject, Tree, Commit, IndexEntry, Blob, RepositoryStatus, Signature, Reference, TreeEntry, \
    Index
from pigit.bean.enum import SpecialReference
from pigit.command import ObjectStoreCommand, ReferenceStoreCommand, Commands
from pigit.configuration_provider import ConfigurationProvider
from pigit.id_generator import IdGenerator
from pigit.staging_area import StagingArea
from pigit.store import ObjectStore, ReferenceStore
from pigit.working_area import WorkingArea


class Repository:
    def __init__(self, object_store: ObjectStore, reference_store: ReferenceStore, working_area: WorkingArea,
                 configuration_provider: ConfigurationProvider, id_generator: IdGenerator, staging_area: StagingArea):
        self.object_store = object_store
        self.reference_store = reference_store
        self.configuration_provider = configuration_provider
        self.working_area = working_area
        self.id_generator = id_generator
        self.staging_area = staging_area

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

    def stage_chunk(self, chunk: bytes):
        pass

    def get_index(self):
        return self.staging_area.get_index()

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

    @property
    def status(self) -> RepositoryStatus:
        return self.get_status()

    def get_status(self) -> RepositoryStatus:
        index = self.index

        changed = set()
        created = set()

        index_entries_by_path = {entry.path: entry for entry in index.entries}

        files_in_working_area = set(self.working_area.get_files())
        for file in files_in_working_area:  # type: Path
            file_path_str = str(file)
            if file_path_str not in index_entries_by_path:
                created.add(file)
            else:
                entry = index_entries_by_path[file_path_str]  # type: IndexEntry
                if self.has_changed(entry):
                    changed.add(file_path_str)

        deleted = set(file for file in index_entries_by_path if Path(file) not in files_in_working_area)
        current_branch = self.reference_store.get_branch_name(self.head)
        return RepositoryStatus(branch_name=current_branch, changed=changed, created=created, deleted=deleted)

    def add(self, filename: str):
        with open(filename, 'rb') as fp:
            content = fp.read()
            # TODO: This should happen via "stage_chunk" method

            # Create blob
            blob = Blob(None, content)
            blob.id = self.id_generator.generate_id(blob)

            self.object_store.store_object(blob)
            self.staging_area.add_to_index(Path(filename), blob.id)

    def commit(self, *, message: str, author: Signature, committer: Signature = None) -> Commit:
        if committer is None:
            committer = author

        try:
            tree = self._generate_tree()
        except IndexNotFoundException:
            raise NothingToCommitException

        head = self.get_head()
        if head.commit is not None:
            last_commit = self.object_store.get_object(head.commit)  # type: Commit
            if last_commit.tree.id == tree.id:
                raise NothingToCommitException

        commit = self._generate_commit(author, committer, message, tree, head)

        commands = Commands([ObjectStoreCommand(self.object_store, commit),
                             ReferenceStoreCommand(self.reference_store, Reference(head.name, commit.id))])

        try:
            commands.execute()
        except:
            commands.rollback()
            raise
        return commit

    def _get_tree_from_index_and_store(self, index: Index) -> Tree:
        parent_stack = [(Path('.'), Tree())]

        for entry in index.entries:
            file_path = Path(entry.path)
            parent = file_path.parent
            if parent != parent_stack[-1][0]:
                while parent_stack[-1][1] not in file_path.parents:
                    current_parent_dir, current_parent_tree = parent_stack[-1]
                    parent_stack.pop()
                    current_parent_tree.id = self.id_generator.generate_id(current_parent_tree)
                    try:
                        self.object_store.store_object(current_parent_tree)
                    except DuplicateObjectException as e:
                        pass
                    parent_stack[-1][1].add_entry(TreeEntry('040000', current_parent_dir.name, current_parent_tree.id))

                paths_to_add = [p for p in reversed(file_path.parents)
                                if p != parent_stack[-1][0] or p not in parent_stack[-1][0].parents]
                for path in paths_to_add:
                    parent_stack.append((path, Tree()))

            tree_entry = TreeEntry(entry.mode, file_path.name, entry.sha1)
            parent_stack[-1][1].add_entry(tree_entry)

        _, tree = parent_stack.pop()
        tree.id = self.id_generator.generate_id(tree)
        try:
            self.object_store.store_object(tree)
        except DuplicateObjectException as e:
            pass

        return tree

    def _generate_tree(self) -> Tree:
        tree = self._get_tree_from_index_and_store(self.staging_area.get_index())
        return tree

    def _generate_commit(self, author, committer, message, tree, head) -> Commit:
        if head.commit is not None:
            parents = [self.object_store.get_object(head.commit)]
        else:
            parents = []
        commit = Commit(None, parents=parents, author=author, committer=committer, commit_message=message, tree=tree)
        commit.id = self.id_generator.generate_id(commit)
        return commit
