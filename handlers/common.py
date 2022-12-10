import csv
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Set, Callable

from gut_settings import GutSettings
from index_objects.index_entry import IndexEntry
from index_objects.tree_entry import TreeEntry
from path_extensions import apply_func_to_batches


class CommonHandler:  # ToDo: Разобрать портянку
    settings = GutSettings

    def __init__(self):
        self.index = self.read_index()
        self.gutignore = self.read_gutignore()

    def get_from_index(
            self, obj_path: Path, dir_hash: Optional[str] = None, entry_type: Optional[IndexEntry.EntryType] = None,
            create_new: Optional[bool] = True
    ) -> Optional[IndexEntry]:
        if obj_path in self.index:
            return self.index[obj_path]
        if create_new:
            if entry_type is None or dir_hash is None:
                raise ValueError
            return IndexEntry(
                file_path=obj_path,
                timestamp=datetime.fromtimestamp(obj_path.lstat().st_mtime),
                dir_hash=dir_hash,
                entry_type=entry_type
            )

    def read_index(self) -> Dict[Path, IndexEntry]:
        with self.settings.INDEX_FILE_PATH.open() as index_file:
            csv_reader = csv.DictReader(index_file, delimiter=self.settings.INDEX_FIELD_DELIMITER)
            index = {}
            for row in csv_reader:
                path = Path(row[IndexEntry.FieldName.FILE_NAME])
                index[path] = IndexEntry(
                    file_path=path, timestamp=row[IndexEntry.FieldName.TIMESTAMP],
                    dir_hash=row[IndexEntry.FieldName.DIR_HASH], stage_hash=row[IndexEntry.FieldName.STAGE_HASH],
                    repo_hash=row[IndexEntry.FieldName.REPO_HASH],
                    entry_type=IndexEntry.EntryType(row[IndexEntry.FieldName.ENTRY_TYPE])
                )

        return index

    def write_index(self) -> None:
        with self.settings.INDEX_FILE_PATH.open(mode='w') as index_file:
            csv_writer = csv.DictWriter(index_file, delimiter=self.settings.INDEX_FIELD_DELIMITER,
                                        fieldnames=list(IndexEntry.FieldName))
            csv_writer.writeheader()
            for file_path in self.index:
                csv_writer.writerow({
                    IndexEntry.FieldName.FILE_NAME: str(file_path),
                    IndexEntry.FieldName.TIMESTAMP: self.index[file_path].timestamp,
                    IndexEntry.FieldName.DIR_HASH: self.index[file_path].dir_hash,
                    IndexEntry.FieldName.STAGE_HASH: self.index[file_path].stage_hash,
                    IndexEntry.FieldName.REPO_HASH: self.index[file_path].repo_hash,
                    IndexEntry.FieldName.ENTRY_TYPE: self.index[file_path].type,
                })

    def read_gutignore(self) -> Set[Path]:  # ToDo check if .gutignore doesn't exist
        res = {self.settings.GUTIGNORE_FILE_PATH, self.settings.GUT_DIR_PATH}
        with self.settings.GUTIGNORE_FILE_PATH.open(mode='r') as gutignore_file:
            for line in gutignore_file.readlines():
                res.add(Path(line.strip()))
        return res

    @classmethod
    def hash_file(cls, file_path: Path) -> str:
        sha1 = hashlib.sha1()
        apply_func_to_batches(file_path, lambda data: sha1.update(data))
        return sha1.hexdigest()

    @classmethod
    def hash_content(cls, content: str) -> str:
        return hashlib.sha1(content.encode()).hexdigest()

    @classmethod
    def write_object(cls, obj_hash: str, content: str) -> None:
        (cls.settings.OBJECTS_DIR_PATH / obj_hash).write_text(content)

    @classmethod
    def serialize_tree_content(
            cls, tree: TreeEntry, filter_func: Optional[Callable[[IndexEntry], bool]] = None
    ) -> str:
        if filter_func is None:
            filter_func = lambda x: True
        return '\n'.join(
            child_entry.to_tree_content_line() for child_entry in filter(filter_func, tree.child_entries)
        )
