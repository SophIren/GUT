from pathlib import Path

from handlers.index_handler import IndexHandler


class TreeWriteHandler(IndexHandler):
    def drop_commited(self, commit_path: Path) -> None:
        pass

    def add_commited(self, commit_path: Path) -> None:
        pass
