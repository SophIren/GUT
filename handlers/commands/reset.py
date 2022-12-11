from pathlib import Path
from typing import Dict

from handlers.branch_info_handler import BranchInfoHandler
from handlers.tree.tree_reader import TreeReadHandler
from index_objects.index_entry import IndexEntry


class ResetHandler(TreeReadHandler, BranchInfoHandler):
    def handle(self, to_commit: str):
        current_objs = self.get_commit_tree(self.OBJECTS_DIR_PATH / self.current_commit)
        to_objs = self.get_commit_tree(self.OBJECTS_DIR_PATH / to_commit)

        for cur_obj in current_objs:
            if cur_obj not in to_objs:
                cur_obj.unlink()
                continue
            if current_objs[cur_obj].repo_hash == to_objs[cur_obj]:
                continue
            if current_objs[cur_obj].type == IndexEntry.EntryType.FILE:
                new_content = self.read_object(to_objs[cur_obj].repo_hash)
                current_objs[cur_obj].file_path.write_text(new_content)
            self.index[cur_obj] = to_objs[cur_obj]

        self.write_index()

    @classmethod
    def get_commit_tree(cls, commit_path: Path) -> Dict[Path, IndexEntry]:
        with commit_path.open() as commit_file:
            _ = commit_file.readline()
            _, tree_hash = commit_file.readline().split()
        res = {}
        for obj_entry in cls.traverse_tree(tree_hash):
            res[Path(obj_entry.file_path)] = obj_entry
        return res
