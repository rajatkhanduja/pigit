from pathlib import Path
from typing import Generator, Union

from pigit.store import ObjectStore
from .working_area import WorkingArea

from pigit.bean import Tree, TreeEntry, Blob


class MemoryWorkingArea(WorkingArea):
    def __init__(self, object_store: ObjectStore, root_dir: Path):
        self.files = []
        self.file_content = {}
        self.object_store = object_store
        self.dir = root_dir

    def get_files(self) -> Generator[Path, None, None]:
        yield from self.files

    def get_file_content(self, filename):
        if filename not in self.file_content:
            raise FileNotFoundError

        return self.file_content[filename]

    def setup(self, snapshot: Tree):
        self.files, self.file_content = self._setup(snapshot, self.dir)

    def _setup(self, snapshot: Tree, path: Path):
        new_files = []
        new_file_content = {}

        for entry in snapshot.entries:  # type: TreeEntry
            git_object = self.object_store.get_object(entry.object_id)  # type: Union[Tree, Blob]

            if type(git_object) == Blob:
                file_path = path / entry.filename
                new_files.append(file_path)
                new_file_content[file_path] = git_object.content
            else:
                self._setup(git_object, path / entry.filename)

        return new_files, new_file_content
