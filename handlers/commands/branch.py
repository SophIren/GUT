import shutil
from pathlib import Path
from typing import Optional, Dict

from handlers.branch_info_handler import BranchInfoHandler
from handlers.commit_info_handler import CommitInfoHandler
from index_objects.index_entry import IndexEntry


class BranchHandler(CommitInfoHandler, BranchInfoHandler):
    def __init__(self):
        CommitInfoHandler.__init__(self)
        BranchInfoHandler.__init__(self)

    def handle(
            self, switch_to: Optional[str] = None,
            create_name: Optional[str] = None,
            rename_to_name: Optional[str] = None,
            delete_name: Optional[str] = None
    ) -> None:
        if switch_to is not None:
            self.checkout(self.get_branch_path(switch_to))
        if create_name is not None:
            self.create_branch(self.get_branch_path(create_name))
        if rename_to_name is not None:
            self.rename_branch(self.current_branch,
                               self.get_branch_path(rename_to_name))
        if delete_name is not None:
            self.delete_branch(self.get_branch_path(delete_name))
        if switch_to == create_name == rename_to_name == delete_name is None:
            self.print_branches()

    def checkout(self, branch_path: Path) -> None:
        to_commit = branch_path.read_text()
        current_objs = self.get_objects_from_commit(self.OBJECTS_DIR_PATH / self.current_commit)
        to_objs = self.get_objects_from_commit(self.OBJECTS_DIR_PATH / to_commit)
        self.remove_and_change_diff(current_objs, to_objs)
        self.add_diff(current_objs, to_objs)

        self.HEAD_FILE_PATH.write_text(str(branch_path))

        self.write_index()

    def remove_and_change_diff(self, current_objs: Dict[Path, IndexEntry], to_objs: Dict[Path, IndexEntry]) -> None:
        for cur_obj in current_objs:
            if cur_obj not in to_objs:
                del self.index[cur_obj]
                if self.index[cur_obj].type == IndexEntry.EntryType.FILE:
                    cur_obj.unlink()
                elif self.index[cur_obj].type == IndexEntry.EntryType.DIRECTORY:
                    shutil.rmtree(cur_obj)
                continue
            if current_objs[cur_obj].repo_hash == to_objs[cur_obj].repo_hash:
                continue
            if current_objs[cur_obj].type == IndexEntry.EntryType.FILE:
                self.write_obj_content_to_file(to_objs[cur_obj].repo_hash, current_objs[cur_obj].file_path)
            self.index[cur_obj] = to_objs[cur_obj]

    def add_diff(self, current_objs: Dict[Path, IndexEntry], to_objs: Dict[Path, IndexEntry]) -> None:
        for cur_obj in to_objs:
            if cur_obj not in current_objs:
                self.write_obj_content_to_file(to_objs[cur_obj].repo_hash, current_objs[cur_obj].file_path)
                self.index[cur_obj] = to_objs[cur_obj]

    def create_branch(self, branch_path: Path) -> None:
        branch_path.write_text(self.current_commit)

    def delete_branch(self, branch_path: Path) -> None:
        if branch_path == self.current_branch:
            raise ValueError("WTF you are on me!")
        if not branch_path.exists():
            raise ValueError("Branch doesn't exist!")
        branch_path.unlink()

    def rename_branch(self, branch_path: Path, new_branch_path: Path) -> None:
        new_branch_path = branch_path.rename(new_branch_path)
        self.HEAD_FILE_PATH.write_text(str(new_branch_path))

    def print_branches(self) -> None:
        print()
        for branch in self.HEADS_DIR_PATH.glob('*'):
            if branch == self.current_branch:
                print(f"{branch.name} <-")
            else:
                print(branch.name)
