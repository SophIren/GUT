from colorama import Fore, Style

from handlers.commit_info_handler import CommitInfoHandler


class SquashHandler(CommitInfoHandler):
    def handle(self, lower_commit: str, upper_commit: str) -> None:
        commit_interval = self.get_commit_interval(lower_commit, upper_commit)
        if not commit_interval:
            print(f"\n{Fore.RED}Wrong interval!!!{Style.RESET_ALL}\n")

        new_parent = self.get_parent_commit_hash(lower_commit)
        self.change_commit_parent(upper_commit, new_parent)

        for commit in commit_interval:
            self.delete_object(commit)
        print(f"\n{Fore.GREEN}Successfully squashed ^_^{Style.RESET_ALL}\n")
