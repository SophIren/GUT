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
        (self.HEADS_DIR_PATH / self.current_commit).write_text(to_commit)

    def remove_and_change_diff_index(
            self, current_objs: Dict[Path, IndexEntry], to_objs: Dict[Path, IndexEntry]
    ) -> None:  # ToDo: Duplicate with branch
        for cur_obj in current_objs:
            if cur_obj not in to_objs:
                del self.index[cur_obj]
                continue
            if current_objs[cur_obj].repo_hash == to_objs[cur_obj].repo_hash:
                continue
            self.index[cur_obj] = to_objs[cur_obj]

    def add_diff_index(
            self, current_objs: Dict[Path, IndexEntry], to_objs: Dict[Path, IndexEntry]
    ) -> None:  # ToDo: Duplicate with branch
        for cur_obj in to_objs:
            if cur_obj not in current_objs:
                self.index[cur_obj] = to_objs[cur_obj]
