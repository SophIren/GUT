from datetime import datetime
from pathlib import Path

from index_objects.index_entry import IndexEntry


class BlobEntry(IndexEntry):
    def __init__(self, file_path: Path, dir_hash: str,
                 timestamp: datetime = datetime.now(),
                 repo_hash: str = '', stage_hash: str = ''):
        super().__init__(file_path=file_path,
                         timestamp=timestamp,
                         dir_hash=dir_hash,
                         entry_type=IndexEntry.EntryType.FILE,
                         repo_hash=repo_hash,
                         stage_hash=stage_hash)
