import shutil
from pathlib import Path

from command_handlers.common import CommonHandler
from index_objects.index_entry import IndexEntry


class AddHandler(CommonHandler):
    def handle(self, path: Path) -> None:
        for obj_entry in self.traverse_obj(path):
            obj_entry.stage_hash = obj_entry.dir_hash
            self.index[obj_entry.file_path] = obj_entry

            if obj_entry.type == IndexEntry.EntryType.FILE:
                shutil.copy(obj_entry.file_path, self.settings.OBJECTS_DIR_PATH / obj_entry.stage_hash)
            if obj_entry.type == IndexEntry.EntryType.DIRECTORY:
                self.write_object(
                    obj_entry.stage_hash,
                    '\n'.join(child_entry.to_tree_content_line() for child_entry in obj_entry.child_entries))

        parent_dir = path.parent
        while parent_dir in self.index:
            parent_entry = next(self.traverse_obj(parent_dir, only_current=True))
            self.index[parent_dir].stage_hash = parent_entry.dir_hash
            parent_dir = parent_dir.parent

        self.write_index()
