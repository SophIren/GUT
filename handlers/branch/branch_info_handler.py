from pathlib import Path

from handlers.common import CommonHandler


class BranchInfoHandler(CommonHandler):
    def __init__(self):
        super().__init__()
        self._current_branch = Path(self.settings.HEAD_FILE_PATH.read_text())

    def get_branch_path(self, branch_name: str) -> Path:
        return self.settings.HEADS_DIR_PATH / branch_name

    @property
    def current_branch(self) -> Path:
        return self._current_branch

    @current_branch.setter
    def current_branch(self, value: str):
        branch_path = Path(self.settings.HEADS_DIR_PATH / value)
        if not branch_path.exists():
            raise ValueError("Branch doesn't exist!")

        self._current_branch = branch_path
        self.settings.HEADS_DIR_PATH.write_text(str(self._current_branch))
