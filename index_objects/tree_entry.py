from datetime import datetime
from pathlib import Path
from typing import List, Optional, Callable

from index_objects.index_entry import IndexEntry


class TreeEntry(IndexEntry):
    def __init__(self, file_path: Path,
                 timestamp: datetime, dir_hash: str,
                 child_entries: List[IndexEntry],
                 repo_hash: str = '', stage_hash: str = ''):
        super().__init__(file_path, timestamp, dir_hash, IndexEntry.EntryType.DIRECTORY,
                         repo_hash=repo_hash, stage_hash=stage_hash)
        self.child_entries = child_entries

    def serialize_content(self, filter_func: Optional[Callable[[IndexEntry], bool]] = None) -> str:
        if filter_func is None:
            filter_func = lambda x: True
        return '\n'.join(
            child_entry.to_tree_content_line() for child_entry in filter(filter_func, self.child_entries)
        )
