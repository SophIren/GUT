from pathlib import Path
from typing import Dict

from handlers.tree.tree_info import TreeInfoHandler
from index_objects.index_entry import IndexEntry


class CommitInfoHandler(TreeInfoHandler):
    @classmethod
    def get_objects_from_commit(cls, commit_path: Path) -> Dict[Path, IndexEntry]:
        with commit_path.open() as commit_file:
            _ = commit_file.readline()
            _, tree_hash = commit_file.readline().split()
        res = {}
        for obj_entry in cls.traverse_tree(tree_hash):
            res[Path(obj_entry.file_path)] = obj_entry
        return res
