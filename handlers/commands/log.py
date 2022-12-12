from colorama import Fore, Style

from handlers.branch_info_handler import BranchInfoHandler
from handlers.commit_info_handler import CommitInfoHandler


class LogHandler(CommitInfoHandler, BranchInfoHandler):
    def __init__(self):
        CommitInfoHandler.__init__(self)
        BranchInfoHandler.__init__(self)

    def handle(self) -> None:
        current_commit = self.current_commit
        arrow = "<<<--------"
        while current_commit:
            print(f"{Fore.GREEN}commit {current_commit} " + arrow + Style.RESET_ALL)
            print(Fore.YELLOW + self.read_object(current_commit) + Style.RESET_ALL)
            print("\n----------------------------\n")
            current_commit = self.get_parent_commit_hash(current_commit)
            arrow = ""
