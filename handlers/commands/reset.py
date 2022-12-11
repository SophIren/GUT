from pathlib import Path
from typing import Dict

from handlers.branch_info_handler import BranchInfoHandler
from handlers.tree.tree_info import TreeInfoHandler
from index_objects.index_entry import IndexEntry


class ResetHandler(TreeInfoHandler, BranchInfoHandler):
    def __init__(self):
        TreeInfoHandler.__init__(self)
        BranchInfoHandler.__init__(self)

    def handle(self, to_commit: str):
        self.reset(to_commit)

    def reset(self, to_commit: str) -> None:
        current_objs = self.get_commit_tree(self.OBJECTS_DIR_PATH / self.current_commit)
        to_objs = self.get_commit_tree(self.OBJECTS_DIR_PATH / to_commit)
        self.remove_and_change_diff(current_objs, to_objs)
        self.add_diff(current_objs, to_objs)

        self.DETACHED_BRANCH_PATH.touch(exist_ok=True)
        self.DETACHED_BRANCH_PATH.write_text(to_commit)
        self.HEAD_FILE_PATH.write_text(str(self.DETACHED_BRANCH_PATH))

        self.write_index()

    def remove_and_change_diff(self, current_objs: Dict[Path, IndexEntry], to_objs: Dict[Path, IndexEntry]) -> None:
        for cur_obj in current_objs:
            if cur_obj not in to_objs:
                cur_obj.unlink()
                continue
            if current_objs[cur_obj].repo_hash == to_objs[cur_obj].repo_hash:
                continue
            if current_objs[cur_obj].type == IndexEntry.EntryType.FILE:
                self.write_obj_to_file(to_objs[cur_obj].repo_hash, current_objs[cur_obj].file_path)
            self.index[cur_obj] = to_objs[cur_obj]

    def add_diff(self, current_objs: Dict[Path, IndexEntry], to_objs: Dict[Path, IndexEntry]) -> None:
        for cur_obj in to_objs:
            if cur_obj not in current_objs:
                self.write_obj_to_file(to_objs[cur_obj].repo_hash, current_objs[cur_obj].file_path)

    @classmethod
    def write_obj_to_file(cls, obj_hash: str, file_path: Path) -> None:
        content = cls.read_object(obj_hash)
        file_path.write_text(content)

    @classmethod
    def get_commit_tree(cls, commit_path: Path) -> Dict[Path, IndexEntry]:
        with commit_path.open() as commit_file:
            _ = commit_file.readline()
            _, tree_hash = commit_file.readline().split()
        res = {}
        for obj_entry in cls.traverse_tree(tree_hash):
            res[Path(obj_entry.file_path)] = obj_entry
        return res
