from pathlib import Path
from typing import List

from index_objects.blob_entry import BlobEntry
from index_objects.index_entry import IndexEntry
from index_objects.tree_entry import TreeEntry


def cast_index_entry_to_blob_entry(index_entry: IndexEntry, path: Path) -> BlobEntry:
    return BlobEntry(
        file_name=index_entry.file_name,
        path=path,
        timestamp=index_entry.timestamp,
        dir_hash=index_entry.dir_hash,
        repo_hash=index_entry.repo_hash,
        stage_hash=index_entry.stage_hash
    )


def cast_index_entry_to_tree_entry(index_entry: IndexEntry, path: Path, child_entries: List[IndexEntry]) -> TreeEntry:
    return TreeEntry(
        file_name=index_entry.file_name,
        path=path,
        timestamp=index_entry.timestamp,
        dir_hash=index_entry.dir_hash,
        repo_hash=index_entry.repo_hash,
        stage_hash=index_entry.stage_hash,
        child_entries=child_entries
    )
