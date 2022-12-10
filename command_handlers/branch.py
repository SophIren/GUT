from pathlib import Path
from typing import Optional

from command_handlers.common import CommonHandler


class BranchHandler(CommonHandler):
    def handle(
            self, switch_to: Optional[str] = None,
            create_name: Optional[str] = None,
            rename_to_name: Optional[str] = None,
            delete_name: Optional[str] = None
    ) -> None:
        if switch_to is not None:
            self.checkout(self.branch_info.get_branch_path(switch_to))
        if create_name is not None:
            self.create_branch(self.branch_info.get_branch_path(create_name))
        if rename_to_name is not None:
            self.rename_branch(self.branch_info.current_branch,
                               self.branch_info.get_branch_path(rename_to_name))
        if delete_name is not None:
            self.delete_branch(self.branch_info.get_branch_path(delete_name))
        if switch_to == create_name == rename_to_name == delete_name is None:
            self.print_branches()

    def checkout(self, branch_path: Path) -> None:
        pass

    def create_branch(self, branch_path: Path) -> None:
        current_commit = self.branch_info.current_branch.read_text()
        branch_path.write_text(current_commit)

    def delete_branch(self, branch_path: Path) -> None:
        if branch_path == self.branch_info.current_branch:
            raise ValueError("WTF you are on me!")
        if not branch_path.exists():
            raise ValueError("Branch doesn't exist!")
        branch_path.unlink()

    def rename_branch(self, branch_path: Path, new_branch_path: Path) -> None:
        new_branch_path = branch_path.rename(new_branch_path)
        self.settings.HEAD_FILE_PATH.write_text(str(new_branch_path))

    def print_branches(self) -> None:
        print()
        for branch in self.settings.HEADS_DIR_PATH.glob('*'):
            if branch == self.branch_info.current_branch:
                print(f"{branch.name} <-")
            else:
                print(branch.name)