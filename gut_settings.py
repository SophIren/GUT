from pathlib import Path


class GutSettings:
    GUT_DIR_PATH: Path = Path(".gut")
    OBJECTS_DIR_PATH: Path = GUT_DIR_PATH / "objects"
    REFS_DIR_PATH: Path = GUT_DIR_PATH / "refs"
    HEADS_DIR_PATH: Path = REFS_DIR_PATH / "heads"

    INDEX_FILE_PATH: Path = GUT_DIR_PATH / "index.csv"
    GUTIGNORE_FILE_PATH: Path = Path(".gutignore")
    HEAD_FILE_PATH: Path = GUT_DIR_PATH / "head.txt"

    DEFAULT_HEAD_FILE_PATH: Path = HEADS_DIR_PATH / "master"

    INDEX_FIELD_DELIMITER: str = ':'
