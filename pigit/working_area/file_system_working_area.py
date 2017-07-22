import shutil

from pathlib import Path
from typing import Union, List, Set
from tempfile import TemporaryDirectory

from pigit.store import ObjectStore
from pigit.bean import Tree, TreeEntry, Blob

from .working_area import WorkingArea


class FileSystemWorkingArea(WorkingArea):
    def __init__(self, object_store: ObjectStore, setup_dir: Path, git_dir: Path, ignore_rules: List[str]):
        self.object_store = object_store
        self.dir = setup_dir
        self.git_dir = git_dir
        self.ignore_rules = ignore_rules

    def setup(self, snapshot: Tree):
        tmp_dir = TemporaryDirectory()
        try:
            if self.dir.exists():
                pass
            self._setup(snapshot, self.dir)
        except:
            pass
        finally:
            tmp_dir.cleanup()

    def get_files(self):
        ignored_files = self.get_ignored_files()
        for p in self.dir.rglob("*"): # type: Path
            if p.is_dir():
                continue
            if not self.to_be_ignored(p, ignored_files):
                yield p.relative_to(self.dir)

    def get_ignored_files(self):
        ignored_files = set()
        for rule in self.ignore_rules:
            for file in self.dir.rglob(rule):
                ignored_files.add(file)
        return ignored_files

    def get_file_content(self, filename: Path):
        with open(self.dir / filename, 'rb') as fp:
            return fp.read()

    def _setup(self, snapshot: Tree, path: Path):
        path.mkdir(exist_ok=True)

        for entry in snapshot.entries:  # type: TreeEntry
            git_object = self.object_store.get_object(entry.object_id)  # type: Union[Tree, Blob]

            if type(git_object) == Blob:
                file_path = path / entry.filename
                with file_path.open('wb') as fp:
                    fp.write(git_object.content)
            else:
                self._setup(git_object, path / entry.filename)

    def to_be_ignored(self, path: Path, ignored_files: Set[Path]) -> bool:
        # TODO: This is definitely not an optimal way to do this.
        assert isinstance(path, Path), f"{path} is not of the required type"

        if self.git_dir in path.parents or path in ignored_files:
            return True

        for parent in path.parents:
            if parent in ignored_files:
                return True

        return False
