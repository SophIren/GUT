import hashlib
from pathlib import Path

from gut_settings import GutSettings
from path_extensions import apply_func_to_batches


class ObjectHandler(GutSettings):
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
        (cls.OBJECTS_DIR_PATH / obj_hash).write_text(content)

    @classmethod
    def read_object(cls, obj_hash: str) -> str:
        return (cls.OBJECTS_DIR_PATH / obj_hash).read_text()

    @classmethod
    def write_obj_content_to_file(cls, obj_hash: str, file_path: Path) -> None:
        content = cls.read_object(obj_hash)
        file_path.write_text(content)
