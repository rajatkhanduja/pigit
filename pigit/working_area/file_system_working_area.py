import shutil

from pathlib import Path
from typing import Union
from tempfile import TemporaryDirectory

from pigit.dal import ObjectStore
from pigit.bean import Tree, TreeEntry, Blob

from .working_area import WorkingArea


class FileSystemWorkingArea(WorkingArea):
    def __init__(self, object_store: ObjectStore, setup_dir):
        self.object_store = object_store
        self.dir = Path(setup_dir)

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

    def _setup(self, snapshot: Tree, path: Path):
        path.mkdir(exist_ok=True)

        for entry in snapshot.entries:  # type: TreeEntry
            git_object = self.object_store.get_object(entry.object_id)  #type: Union[Tree, Blob]

            if type(git_object) == Blob:
                file_path = path / entry.filename
                with file_path.open('wb') as fp:
                    fp.write(git_object.content)
            else:
                self._setup(git_object, path / entry.filename)
