from enum import Enum
from pathlib import Path
from typing import List

from command_handlers.common import CommonHandler


class StatusHandler(CommonHandler):
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
            if obj_entry.path == Path('.'):
                continue
            if obj_entry.file_name not in self.index:
                excluded.append(str(obj_entry.path))
            elif self.index[obj_entry.file_name].stage_hash != obj_entry.dir_hash:
                modified.append(str(obj_entry.path))
            elif self.index[obj_entry.file_name].repo_hash != obj_entry.dir_hash:
                gut.append(str(obj_entry.path))

        self.write_index()
        self.pprint(excluded, modified, gut)

    @classmethod
    def pprint(cls, excluded: List[str], modified: List[str], gut: List[str]):
        if excluded:
            print(f"\n{cls.Colors.FAIL}Very not gut!!!{cls.Colors.ENDC}\nAdd to index with gut add")
            print(f"{cls.Colors.FAIL}    " + '\n    '.join(excluded) + cls.Colors.ENDC)

        if modified:
            print(f"\n{cls.Colors.WARNING}Not gut!!! These are modified.{cls.Colors.ENDC}\nAdd to index with gut add")
            print(f"{cls.Colors.WARNING}    " + '\n    '.join(modified) + cls.Colors.ENDC)

        if gut:
            print(f"\n{cls.Colors.OKGREEN}Very very gut ^_^")
            print("    " + '\n    '.join(gut) + cls.Colors.ENDC)
