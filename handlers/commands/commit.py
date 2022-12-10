from datetime import datetime
from pathlib import Path

from handlers.branch import BranchInfoHandler
from handlers.tree.tree_reader import TreeReadHandler
from index_objects.index_entry import IndexEntry


class CommitHandler(BranchInfoHandler, TreeReadHandler):
    def handle(self, path: Path, message: str) -> None:
        self.index[Path('.')] = IndexEntry(Path('.'), datetime.now(), '', entry_type=IndexEntry.EntryType.DIRECTORY)
        root_dir_entry = next(self.traverse_obj(Path('.'), only_current=True, only_staged=True))
        del self.index[Path('.')]
        self.write_object(root_dir_entry.dir_hash, self.serialize_tree_content(root_dir_entry))

        for obj_entry in filter(lambda com_obj: com_obj.file_path in self.index, self.traverse_obj(path)):
            obj_entry.repo_hash = obj_entry.stage_hash
            self.index[obj_entry.file_path] = obj_entry

        parent_dir = path.parent
        while parent_dir in self.index:
            parent_entry = next(self.traverse_obj(parent_dir, only_current=True, only_staged=True))
            self.index[parent_dir].repo_hash = parent_entry.stage_hash
            parent_dir = parent_dir.parent

        current_commit = self.current_branch.read_text()
        commit_content = self.get_commit_content(message, root_dir_entry.dir_hash, current_commit)
        commit_hash = self.hash_content(commit_content)
        self.write_head(commit_hash)
        self.write_object(commit_hash, commit_content)

        self.write_index()

    def read_head(self) -> str:
        return self.settings.HEAD_FILE_PATH.read_text()

    def write_head(self, head_hash: str) -> None:
        self.current_branch.write_text(head_hash)

    @classmethod
    def get_commit_content(cls, message: str, root_dir_hash: str, parent_hash: str) -> str:
        return f"parent {parent_hash}\ntree {root_dir_hash}\n\n{message}"
