from pathlib import Path
from typing import List
from colorama import Fore, Style

from handlers.branch_info_handler import BranchInfoHandler
from handlers.tree.tree_info import TreeInfoHandler
from index_objects.index_entry import IndexEntry


class StatusHandler(BranchInfoHandler, TreeInfoHandler):
    def handle(self) -> None:
        excluded: List[str] = []
        modified: List[str] = []
        gut: List[str] = []
        for obj_entry in self.traverse_obj(Path('.')):
            if obj_entry.file_path == Path('.'):
                continue
            if obj_entry.file_path.parent not in self.index and obj_entry.file_path.parent != Path('.'):
                continue
            if obj_entry.file_path not in self.index:
                excluded.append(str(obj_entry.file_path))
                continue
            if obj_entry.type == IndexEntry.EntryType.DIRECTORY:
                continue

            index_entry = self.index[obj_entry.file_path]
            if index_entry.stage_hash != obj_entry.dir_hash:
                modified.append(str(obj_entry.file_path))
            elif index_entry.repo_hash != obj_entry.dir_hash:
                gut.append(str(obj_entry.file_path))

        self.write_index()
        self.pprint(excluded, modified, gut, self.current_branch.name)

    @classmethod
    def pprint(cls, excluded: List[str], modified: List[str], gut: List[str], current_branch: str):
        print(f"\nOn branch {current_branch}\n")

        if excluded:
            print(f"\n{Fore.RED}Very not gut!!!{Style.RESET_ALL}\nAdd to index with gut add")
            print(f"{Fore.RED}    " + '\n    '.join(excluded) + Style.RESET_ALL)

        if modified:
            print(f"\n{Fore.LIGHTRED_EX}Not gut!!! These are modified.{Style.RESET_ALL}\nAdd to index with gut add")
            print(f"{Fore.LIGHTRED_EX}    " + '\n    '.join(modified) + Style.RESET_ALL)

        if gut:
            print(f"\n{Fore.GREEN}Very very gut ^_^")
            print("    " + '\n    '.join(gut) + Style.RESET_ALL)
