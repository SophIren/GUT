from datetime import datetime
from pathlib import Path

from index_objects.index_entry import IndexEntry


class BlobEntry(IndexEntry):
    def __init__(self, file_name: str, path: Path,
                 timestamp: datetime, dir_hash: str,
                 repo_hash: str = '', stage_hash: str = ''):
        super().__init__(file_name, timestamp, dir_hash, IndexEntry.EntryType.FILE, repo_hash, stage_hash)
        self.path = path
