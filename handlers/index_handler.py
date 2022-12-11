import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from handlers.gutignore_handler import GutignoreHandler
from index_objects.index_entry import IndexEntry


class IndexHandler(GutignoreHandler):
    def __init__(self):
        super().__init__()
        self.index = self.read_index()

    def get_from_index(
            self, obj_path: Path, dir_hash: Optional[str] = None,
            entry_type: Optional[IndexEntry.EntryType] = None,
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
        with self.INDEX_FILE_PATH.open() as index_file:
            csv_reader = csv.DictReader(index_file, delimiter=self.INDEX_FIELD_DELIMITER)
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
        with self.INDEX_FILE_PATH.open(mode='w') as index_file:
            csv_writer = csv.DictWriter(index_file, delimiter=self.INDEX_FIELD_DELIMITER,
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
