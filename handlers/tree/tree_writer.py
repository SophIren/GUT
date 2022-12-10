from pathlib import Path

from handlers.common import CommonHandler


class TreeWriteHandler(CommonHandler):
    def drop_commited(self, commit_path: Path):
        pass

    def add_commited(self, commit_path: Path):
        pass
