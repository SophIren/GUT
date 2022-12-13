from pathlib import Path


class GutSettings:
    INDEX_FIELD_DELIMITER: str = ':'

    GUT_DIR_PATH: Path = Path('.gut')

    @property
    def objects_dir_path(self) -> Path:
        return self.GUT_DIR_PATH / "objects"

    @property
    def refs_dir_path(self) -> Path:
        return self.GUT_DIR_PATH / "refs"

    @property
    def heads_dir_path(self) -> Path:
        return self.refs_dir_path / "heads"

    @property
    def index_file_path(self) -> Path:
        return self.GUT_DIR_PATH / "index.csv"

    @property
    def gutignore_file_path(self) -> Path:
        return Path(".gutignore")

    @property
    def head_file_path(self) -> Path:
        return self.GUT_DIR_PATH / "head.txt"

    @property
    def default_head_file_path(self) -> Path:
        return self.heads_dir_path / "master"
