from pathlib import Path


class GutSettings:
    GUT_DIR_PATH: Path = Path(".gut")
    OBJECTS_DIR_PATH: Path = Path(GUT_DIR_PATH / "objects")
    INDEX_FILE_PATH: Path = Path(GUT_DIR_PATH / "index.csv")
    GUTIGNORE_FILE_PATH: Path = Path(".gutignore")

    INDEX_FIELD_DELIMITER: str = ':'
