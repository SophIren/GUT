from pathlib import Path
from typing import Tuple, Generator

from handlers.tree.tree_info import TreeInfoHandler
from index_objects.index_entry import IndexEntry


class TreeWriteHandler(TreeInfoHandler):
    def drop_unchanged_commited(self, tree_obj_path: Path) -> None:
        self.update_index()  # Todo: Поставить это вместо traverse_obj в add и status
        for obj_type, obj_hash, obj_path in TreeWriteHandler.parse_tree(tree_obj_path):
            index_entry = self.index[obj_path]
            if index_entry.dir_hash == index_entry.repo_hash:
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
