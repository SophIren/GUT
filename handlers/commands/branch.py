import shutil
from pathlib import Path
from typing import Optional, Dict

from colorama import Fore, Style

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
        current_objs = self.get_objects_from_commit(self.objects_dir_path / self.current_commit)
        to_objs = self.get_objects_from_commit(self.objects_dir_path / to_commit)
        self.remove_and_change_diff(current_objs, to_objs)
        self.add_diff(current_objs, to_objs)

        self.head_file_path.write_text(str(branch_path))

        self.write_index()

    def remove_and_change_diff(
            self, current_entries: Dict[Path, IndexEntry], to_entries: Dict[Path, IndexEntry]
    ) -> None:
        for cur_entry in current_entries:
            if cur_entry not in to_entries:
                self.remove_entry(cur_entry)
                continue
            if current_entries[cur_entry].repo_hash == to_entries[cur_entry].repo_hash:
                continue
            if current_entries[cur_entry].type == IndexEntry.EntryType.FILE:
                self.write_obj_content_to_file(to_entries[cur_entry].repo_hash, current_entries[cur_entry].file_path)
            self.index[cur_entry] = to_entries[cur_entry]

    def add_diff(self, current_entries: Dict[Path, IndexEntry], to_entries: Dict[Path, IndexEntry]) -> None:
        for cur_obj in to_entries:
            if cur_obj not in current_entries:
                if to_entries[cur_obj].type == IndexEntry.EntryType.FILE:
                    self.write_obj_content_to_file(to_entries[cur_obj].repo_hash, cur_obj)
                elif to_entries[cur_obj].type == IndexEntry.EntryType.DIRECTORY:
                    cur_obj.mkdir(exist_ok=True)
                self.index[cur_obj] = to_entries[cur_obj]

    def remove_entry(self, entry_path: Path) -> None:
        if self.index[entry_path].type == IndexEntry.EntryType.FILE:
            if entry_path.exists():
                entry_path.unlink()
        elif self.index[entry_path].type == IndexEntry.EntryType.DIRECTORY:
            shutil.rmtree(entry_path)
        del self.index[entry_path]

    def create_branch(self, branch_path: Path) -> None:
        if not self.current_commit:
            raise ValueError("No commit has been made")
        branch_path.write_text(self.current_commit)

    def delete_branch(self, branch_path: Path) -> None:
        if branch_path == self.current_branch:
            raise ValueError("WTF you are on me!")
        if not branch_path.exists():
            raise ValueError("Branch doesn't exist!")
        branch_path.unlink()

    def rename_branch(self, branch_path: Path, new_branch_path: Path) -> None:
        new_branch_path = branch_path.rename(new_branch_path)
        self.head_file_path.write_text(str(new_branch_path))

    def print_branches(self) -> None:
        print()
        for branch in self.heads_dir_path.glob('*'):
            if branch == self.current_branch:
                print(f"{Fore.GREEN}{branch.name}  <<----{Style.RESET_ALL}")
            else:
                print(branch.name)
