import csv
import hashlib
from pathlib import Path
from typing import Dict, Iterable

from gut_settings import GutSettings
from index_entry import IndexEntry


class CommonHandler:
    settings = GutSettings

    @classmethod
    def read_index(cls) -> Dict[str, IndexEntry]:
        with cls.settings.INDEX_FILE.open() as index_file:
            csv_reader = csv.DictReader(index_file, delimiter=cls.settings.INDEX_FIELD_DELIMITER)
            index = {}
            for row in csv_reader:
                index[row[IndexEntry.FieldName.FILE_NAME]] = IndexEntry(
                    file_name=row[IndexEntry.FieldName.FILE_NAME], timestamp=row[IndexEntry.FieldName.TIMESTAMP],
                    dir_hash=row[IndexEntry.FieldName.DIR_HASH], stage_hash=row[IndexEntry.FieldName.STAGE_HASH],
                    repo_hash=row[IndexEntry.FieldName.REPO_HASH],
                    entry_type=IndexEntry.EntryType(row[IndexEntry.FieldName.ENTRY_TYPE])
                )

        return index

    @classmethod
    def write_index(cls, index: Dict[str, IndexEntry]) -> None:
        with cls.settings.INDEX_FILE.open(mode='w') as index_file:
            csv_writer = csv.DictWriter(index_file, delimiter=cls.settings.INDEX_FIELD_DELIMITER,
                                        fieldnames=list(IndexEntry.FieldName))
            csv_writer.writeheader()
            for file_name in index:
                csv_writer.writerow({
                    IndexEntry.FieldName.FILE_NAME: file_name,
                    IndexEntry.FieldName.TIMESTAMP: index[file_name].timestamp,
                    IndexEntry.FieldName.DIR_HASH: index[file_name].dir_hash,
                    IndexEntry.FieldName.STAGE_HASH: index[file_name].stage_hash,
                    IndexEntry.FieldName.REPO_HASH: index[file_name].repo_hash,
                    IndexEntry.FieldName.ENTRY_TYPE: index[file_name].type,
                })

    @classmethod
    def index_is_empty(cls) -> bool:
        with cls.settings.INDEX_FILE.open() as index_file:
            return not index_file.read(1)

    @classmethod
    def read_file_in_batches(cls, file_path: Path) -> Iterable[bytes]:
        with file_path.open(mode='rb') as file:
            while True:
                data = file.read(cls.settings.BUFFER_SIZE)
                if not data:
                    break
                yield data

    @classmethod
    def get_file_sha_1(cls, file_path: Path) -> str:
        sha1 = hashlib.sha1()
        for batch in cls.read_file_in_batches(file_path):
            sha1.update(batch)
        return sha1.hexdigest()

    @classmethod
    def copy_file(cls, from_path: Path, to_path: Path) -> None:
        with to_path.open(mode='w') as to_file:
            for batch in cls.read_file_in_batches(from_path):
                to_file.write(batch.decode())

    @classmethod
    def write_object(cls, obj_hash: str, content: str):
        with (cls.settings.OBJECTS_DIR / obj_hash).open(mode='w') as obj_file:
            obj_file.write(content)
