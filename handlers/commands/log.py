from handlers.branch_info_handler import BranchInfoHandler
from handlers.object_handler import ObjectHandler

from colorama import Fore, Style


class LogHandler(BranchInfoHandler, ObjectHandler):
    def handle(self) -> None:
        current_commit = self.current_commit
        arrow = "<<<--------"
        while current_commit:
            print(f"{Fore.GREEN}commit {current_commit} " + arrow + Style.RESET_ALL)
            print(Fore.YELLOW + self.read_object(current_commit) + Style.RESET_ALL)
            print("\n----------------------------\n")
            current_commit = self.get_parent_commit_hash(current_commit)
            arrow = ""

    @classmethod
    def get_parent_commit_hash(cls, commit_hash: str):
        with (cls.OBJECTS_DIR_PATH / commit_hash).open() as commit_file:
            line = commit_file.readline().split()
            if len(line) == 1:
                return ''
            return line[1]
