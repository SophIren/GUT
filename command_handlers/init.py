import csv

from command_handlers.common import CommonHandler
from index_entry import IndexEntry


class InitHandler(CommonHandler):
    @classmethod
    def handle(cls) -> None:
        cls.settings.OBJECTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.settings.INDEX_FILE.touch(exist_ok=True)

        if not cls.index_is_empty():
            return
        cls.write_index_header()

    @classmethod
    def write_index_header(cls) -> None:
        with cls.settings.INDEX_FILE.open(mode='w') as index_file:
            writer = csv.DictWriter(index_file, fieldnames=list(IndexEntry.FieldName),
                                    delimiter=cls.settings.INDEX_FIELD_DELIMITER)
            writer.writeheader()
