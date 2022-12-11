from pathlib import Path
from typing import Tuple, Generator

from handlers.index_handler import IndexHandler
from index_objects.index_entry import IndexEntry


class TreeWriteHandler(IndexHandler):
    def drop_unchanged_commited(self, tree_obj_path: Path) -> None:
        for obj_type, obj_hash, obj_path in TreeWriteHandler.parse_tree(tree_obj_path):
            index_entry = self.index[obj_path]
            if index_entry:
                pass

    @staticmethod
    def parse_tree(tree_obj_path: Path) -> Generator[Tuple[IndexEntry.EntryType, str, Path]]:
        for obj_line in tree_obj_path.open():
            obj_type_str, obj_hash, obj_path_str = obj_line.split()
            obj_type = IndexEntry.EntryType(obj_type_str)
            obj_path = Path(obj_path_str)
            yield obj_type, obj_hash, obj_path

    def add_commited(self, commit_path: Path) -> None:
        pass
