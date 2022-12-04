from pathlib import Path
from typing import Iterable

from command_handlers.common import CommonHandler
from index_objects.index_entry import IndexEntry


class CommitHandler(CommonHandler):
    def handle(self, path: Path, message: str) -> None:
        head_hash = self.read_head()
        commit_objects = list(filter(lambda com_obj: com_obj.file_name in self.index, self.traverse_obj(path)))
        commit_content = self.get_commit_content(message, commit_objects, head_hash)
        commit_hash = self.hash_content(commit_content)

        for obj in commit_objects:
            self.index[obj.file_name].repo_hash = obj.stage_hash

        self.write_head(commit_hash)
        self.write_index()
        self.write_object(commit_hash, commit_content)

    @classmethod
    def read_head(cls) -> str:
        with cls.settings.HEAD_FILE_PATH.open() as head_file:
            return head_file.read()

    @classmethod
    def write_head(cls, head_hash) -> None:
        with cls.settings.HEAD_FILE_PATH.open(mode='w') as head_file:
            head_file.write(head_hash)

    @classmethod
    def get_commit_content(cls, message: str, index_objects: Iterable[IndexEntry], parent_hash: str) -> str:
        lines = [f"parent {parent_hash}"] if parent_hash else []
        for obj in index_objects:
            lines.append(f"{obj.type} {obj.stage_hash}")
        return '\n'.join(lines) + f"\n\n{message}"
