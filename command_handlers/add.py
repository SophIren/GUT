import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict

from command_handlers.common import CommonHandler
from index_entry import IndexEntry


class AddHandler(CommonHandler):
    @classmethod
    def handle(cls, path: Path) -> None:  # ToDo Убрать говнокода навалило пиздец
        index = cls.read_index()
        if path.is_file():
            index[path.name].stage_hash = cls.get_file_sha_1(path)
            return
        obj_hash = cls.update_index_dir_sha_1(path, index)
        if path.name not in index:
            index[path.name] = IndexEntry(
                file_name=path.name, timestamp=datetime.fromtimestamp(path.lstat().st_mtime),
                dir_hash=obj_hash, stage_hash=obj_hash, repo_hash='',
                entry_type=IndexEntry.EntryType.DIRECTORY)
        index[path.name].stage_hash = obj_hash
        cls.write_index(index)

    @classmethod
    def update_index_dir_sha_1(cls, dir_path: Path,
                               index: Dict[str, IndexEntry]) -> str:  # ToDo: Make acceptable for status|| + timestamp?
        obj_content_lines = []
        for elem in dir_path.glob('*'):
            if elem.is_dir():
                elem_hash = cls.update_index_dir_sha_1(elem, index)
                elem_type = "tree"
            else:
                elem_hash = cls.get_file_sha_1(elem)
                elem_type = "blob"
                cls.copy_file(elem, cls.settings.OBJECTS_DIR / elem_hash)

            obj_content_lines.append(f"{elem_type} {elem_hash} {elem.name}")
            if elem.name not in index:
                index[elem.name] = IndexEntry(
                    file_name=elem.name, timestamp=datetime.fromtimestamp(elem.lstat().st_mtime),
                    dir_hash=elem_hash, stage_hash=elem_hash, repo_hash='',
                    entry_type=IndexEntry.EntryType(elem_type))
            index[elem.name].stage_hash = elem_hash

        obj_content = '\n'.join(obj_content_lines)
        obj_hash = hashlib.sha1(obj_content.encode()).hexdigest()
        cls.write_object(obj_hash, obj_content)

        return obj_hash
