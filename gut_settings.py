from pathlib import Path


class GutSettings:
    GUT_DIR_PATH: Path = Path(".gut")
    OBJECTS_DIR_PATH: Path = GUT_DIR_PATH / "objects"
    INDEX_FILE_PATH: Path = GUT_DIR_PATH / "index.csv"
    GUTIGNORE_FILE_PATH: Path = Path(".gutignore")
    HEAD_FILE_PATH = GUT_DIR_PATH / "head.txt"

    INDEX_FIELD_DELIMITER: str = ':'
