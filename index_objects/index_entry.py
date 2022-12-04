from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path


class IndexEntry:
    class FieldName(str, Enum):
        FILE_NAME = "file_name"
        TIMESTAMP = "timestamp"
        DIR_HASH = "dir_hash"
        STAGE_HASH = "stage_hash"
        REPO_HASH = "repo_hash"
        ENTRY_TYPE = "entry_type"

    class EntryType(str, Enum):
        FILE = "blob"
        DIRECTORY = "tree"

    def __init__(self, file_path: Path, timestamp: datetime,
                 dir_hash: str, entry_type: IndexEntry.EntryType,
                 repo_hash: str = '', stage_hash: str = ''):
        self.file_path = file_path
        self.timestamp = timestamp
        self.dir_hash = dir_hash
        self.stage_hash = stage_hash
        self.repo_hash = repo_hash
        self.type = entry_type

    def to_tree_content_line(self) -> str:
        return f"{self.type} {self.stage_hash} {self.file_path}"
