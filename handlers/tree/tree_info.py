from pathlib import Path
from typing import Optional, List, Iterator, Union

from handlers.object_handler import ObjectHandler
from handlers.index_handler import IndexHandler
from index_objects.blob_entry import BlobEntry
from index_objects.casts import cast_index_entry_to_blob_entry, cast_index_entry_to_tree_entry
from index_objects.index_entry import IndexEntry
from index_objects.tree_entry import TreeEntry


class TreeInfoHandler(IndexHandler, ObjectHandler):
    def traverse_obj(
            self, obj_path: Path,
            only_current: bool = False,
            only_staged: bool = False,
    ) -> Iterator[Union[BlobEntry, TreeEntry]]:  # ToDo: Переделать после переноса на update_index
        if obj_path in self.gutignore:
            return

        is_dir = obj_path.is_dir()
        if not is_dir:
            dir_hash = self.hash_file(obj_path)
            index_entry = self.get_from_index(obj_path, dir_hash=dir_hash,
                                              entry_type=IndexEntry.EntryType.FILE,
                                              create_new=not only_staged)
            if index_entry is None:
                return
            index_entry.dir_hash = dir_hash
            yield cast_index_entry_to_blob_entry(index_entry)
            return

        child_entries: List[IndexEntry] = []
        for child_obj_path in obj_path.glob('*'):
            last_child_index_entry: Optional[IndexEntry] = None
            for child_index_entry in self.traverse_obj(child_obj_path, only_staged=only_staged):
                last_child_index_entry = child_index_entry
                if not only_current:
                    yield child_index_entry
            if last_child_index_entry is not None:
                child_entries.append(last_child_index_entry)
        dir_hash = self.hash_content('\n'.join(child_entry.to_tree_content_line() for child_entry in child_entries))
        index_entry = self.get_from_index(obj_path, dir_hash=dir_hash,
                                          entry_type=IndexEntry.EntryType.DIRECTORY,
                                          create_new=not only_staged)
        if index_entry is None:
            return
        index_entry.dir_hash = dir_hash
        yield cast_index_entry_to_tree_entry(index_entry, child_entries=child_entries)

    @classmethod
    def traverse_tree(cls, tree_hash: str) -> Iterator[IndexEntry]:
        with (cls.OBJECTS_DIR_PATH / tree_hash).open() as tree_file:
            for line in tree_file:
                obj_type_str, obj_hash, obj_path = line.split()
                obj_type = IndexEntry.EntryType(obj_type_str)
                yield IndexEntry(entry_type=IndexEntry.EntryType(obj_type_str),
                                 dir_hash=obj_hash, repo_hash=obj_hash, stage_hash=obj_hash,
                                 file_path=Path(obj_path))
                if obj_type == IndexEntry.EntryType.DIRECTORY:
                    for obj in cls.traverse_tree(obj_hash):
                        yield obj

    def update_index(self):
        for _ in self.traverse_obj(Path('.')):
            pass
        self.write_index()
