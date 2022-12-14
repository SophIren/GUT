from pathlib import Path
from typing import Dict, List

from handlers.tree.tree_info import TreeInfoHandler
from index_objects.index_entry import IndexEntry


class CommitInfoHandler(TreeInfoHandler):
    def get_objects_from_commit(self, commit_path: Path) -> Dict[Path, IndexEntry]:
        with commit_path.open() as commit_file:
            _ = commit_file.readline()
            _, tree_hash = commit_file.readline().split()
        res = {}
        for obj_entry in self.traverse_tree(tree_hash):
            res[Path(obj_entry.file_path)] = obj_entry
        return res

    def get_parent_commit_hash(self, commit_hash: str) -> str:
        with self.get_object_path(commit_hash).open() as commit_file:
            line = commit_file.readline().split()
            if len(line) == 1:
                return ''
            return line[1]

    def get_commit_interval(self, lower_commit_hash: str, upper_commit_hash: str) -> List[str]:
        res = []
        current_commit = self.get_parent_commit_hash(upper_commit_hash)
        while current_commit != lower_commit_hash:
            res.append(current_commit)
            if not current_commit:
                return []
            current_commit = self.get_parent_commit_hash(current_commit)
        res.append(lower_commit_hash)
        return res

    def change_commit_parent(self, commit_hash: str, new_parent_hash: str) -> None:
        with self.get_object_path(commit_hash).open() as commit_file:
            commit_lines = commit_file.readlines()
        commit_lines[0] = f"parent {new_parent_hash}\n"
        with self.get_object_path(commit_hash).open(mode='w') as commit_file:
            commit_file.writelines(commit_lines)
