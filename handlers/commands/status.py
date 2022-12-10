from enum import Enum
from pathlib import Path
from typing import List

from handlers.branch_info_handler import BranchInfoHandler
from handlers.tree.tree_reader import TreeReadHandler


class StatusHandler(BranchInfoHandler, TreeReadHandler):
    class Colors(str, Enum):
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

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

            index_entry = self.index[obj_entry.file_path]
            if index_entry.stage_hash != obj_entry.dir_hash:
                modified.append(str(obj_entry.file_path))
            elif index_entry.repo_hash != obj_entry.dir_hash and index_entry.type == index_entry.EntryType.FILE:
                gut.append(str(obj_entry.file_path))

        self.write_index()
        self.pprint(excluded, modified, gut, self.current_branch.name)

    @classmethod
    def pprint(cls, excluded: List[str], modified: List[str], gut: List[str], current_branch: str):
        print(f"\nOn branch {current_branch}\n")

        if excluded:
            print(f"\n{cls.Colors.FAIL}Very not gut!!!{cls.Colors.ENDC}\nAdd to index with gut add")
            print(f"{cls.Colors.FAIL}    " + '\n    '.join(excluded) + cls.Colors.ENDC)

        if modified:
            print(f"\n{cls.Colors.WARNING}Not gut!!! These are modified.{cls.Colors.ENDC}\nAdd to index with gut add")
            print(f"{cls.Colors.WARNING}    " + '\n    '.join(modified) + cls.Colors.ENDC)

        if gut:
            print(f"\n{cls.Colors.OKGREEN}Very very gut ^_^")
            print("    " + '\n    '.join(gut) + cls.Colors.ENDC)
