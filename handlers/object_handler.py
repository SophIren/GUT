import hashlib
from pathlib import Path

from gut_settings import GutSettings
from path_extensions import apply_func_to_batches


class ObjectHandler(GutSettings):
    @staticmethod
    def hash_file(file_path: Path) -> str:
        sha1 = hashlib.sha1()
        apply_func_to_batches(file_path, lambda data: sha1.update(data))
        return sha1.hexdigest()

    @staticmethod
    def hash_content(content: str) -> str:
        return hashlib.sha1(content.encode()).hexdigest()

    def get_object_path(self, obj_hash: str) -> Path:
        return self.objects_dir_path / obj_hash

    def write_object(self, obj_hash: str, content: str) -> None:
        self.get_object_path(obj_hash).write_text(content)

    def delete_object(self, obj_hash: str) -> None:
        self.get_object_path(obj_hash).unlink()

    def read_object(self, obj_hash: str) -> str:
        return self.get_object_path(obj_hash).read_text()

    def write_obj_content_to_file(self, obj_hash: str, file_path: Path) -> None:
        content = self.read_object(obj_hash)
        file_path.write_text(content)
