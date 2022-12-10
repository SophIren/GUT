from pathlib import Path
from typing import Iterable

from command_handlers.common import CommonHandler
from index_objects.index_entry import IndexEntry


class CommitHandler(CommonHandler):
    def handle(self, path: Path, message: str) -> None:
        current_commit = self.branch_info.current_branch.read_text()
        commit_objects = list(filter(lambda com_obj: com_obj.file_path in self.index, self.traverse_obj(path)))
        commit_content = self.get_commit_content(message, commit_objects, current_commit)
        commit_hash = self.hash_content(commit_content)

        for obj in commit_objects:
            self.index[obj.file_path].repo_hash = obj.stage_hash

        self.write_head(commit_hash)
        self.write_index()
        self.write_object(commit_hash, commit_content)

    def read_head(self) -> str:
        return self.settings.HEAD_FILE_PATH.read_text()

    def write_head(self, head_hash: str) -> None:
        self.branch_info.current_branch.write_text(head_hash)

    @classmethod
    def get_commit_content(cls, message: str, index_objects: Iterable[IndexEntry], parent_hash: str) -> str:
        lines = [f"parent {parent_hash}"] if parent_hash else []
        for obj in index_objects:
            lines.append(f"{obj.type} {obj.stage_hash}")
        return '\n'.join(lines) + f"\n\n{message}"
