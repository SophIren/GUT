from datetime import datetime
from enum import Enum


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

    def __init__(self, file_name: str, timestamp: datetime,
                 dir_hash: str, stage_hash: str,
                 repo_hash: str, entry_type: EntryType):
        self.file_name = file_name
        self.timestamp = timestamp
        self.dir_hash = dir_hash
        self.stage_hash = stage_hash
        self.repo_hash = repo_hash
        self.type = entry_type
