from pathlib import Path


class GutSettings:
    GUT_DIR: Path = Path(".gut")
    OBJECTS_DIR: Path = Path(GUT_DIR / "objects")
    INDEX_FILE: Path = Path(GUT_DIR / "index.csv")

    INDEX_FIELD_DELIMITER: str = ':'
