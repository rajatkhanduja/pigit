from pathlib import Path

from pigit.exception import IndexNotFoundException
from pigit.bean import Index, IndexEntry
from .staging_area import StagingArea


class MemoryStagingArea(StagingArea):
    def __init__(self, working_dir: Path):
        self.index = None   # type: Index
        self.dir = working_dir

    def get_index(self) -> Index:
        if self.index is None:
            raise IndexNotFoundException
        return self.index

    def add_to_index(self, file: Path, generated_id: str):
        if self.index is None:
            self.index = Index('DIRC', 2)

        assert file.is_file()

        if self.dir is not None:
            relative_path = file.relative_to(self.dir)
        else:
            relative_path = file
        self.index.add_index_entry(IndexEntry.from_file(file, generated_id, str(relative_path)))

