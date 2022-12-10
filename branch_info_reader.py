from pathlib import Path


class BranchInfoReader:
    def __init__(self, head_file_path: Path, heads_dir_path: Path):
        self.head_file_path = head_file_path
        self.heads_dir_path = heads_dir_path
        self._current_branch = Path(head_file_path.read_text())

    def get_branch_path(self, branch_name: str) -> Path:
        return self.heads_dir_path / branch_name

    @property
    def current_branch(self) -> Path:
        return self._current_branch

    @current_branch.setter
    def current_branch(self, value: str):
        branch_path = Path(self.heads_dir_path / value)
        if not branch_path.exists():
            raise ValueError("Branch doesn't exist!")

        self._current_branch = branch_path
        self.heads_dir_path.write_text(str(self._current_branch))
