import shutil
from pathlib import Path

from handlers.tree.tree_info import TreeInfoHandler
from index_objects.index_entry import IndexEntry


class AddHandler(TreeInfoHandler):
    def handle(self, path: Path) -> None:
        for obj_entry in self.traverse_obj(path):
            obj_entry.stage_hash = obj_entry.dir_hash
            self.index[obj_entry.file_path] = obj_entry

            if obj_entry.type == IndexEntry.EntryType.FILE:
                shutil.copy(obj_entry.file_path, self.objects_dir_path / obj_entry.stage_hash)
            if obj_entry.type == IndexEntry.EntryType.DIRECTORY:
                self.write_object(obj_entry.stage_hash, obj_entry.serialize_content())

        parent_dir = path.parent
        while parent_dir != self.GUT_DIR_PATH.parent:
            self.index[parent_dir] = IndexEntry(file_path=parent_dir, dir_hash='',
                                                entry_type=IndexEntry.EntryType.DIRECTORY)
            parent_entry = next(self.traverse_obj(parent_dir, only_current=True, only_staged=True))

            self.index[parent_dir].stage_hash = parent_entry.dir_hash
            self.index[parent_dir].dir_hash = parent_entry.dir_hash
            parent_entry.stage_hash = parent_entry.dir_hash

            self.write_object(parent_entry.stage_hash, parent_entry.serialize_content())
            parent_dir = parent_dir.parent

        self.write_index()
