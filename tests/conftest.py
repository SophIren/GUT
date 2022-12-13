from pathlib import Path
import pytest

from gut_settings import GutSettings


@pytest.fixture()
def test_dir_path() -> Path:
    return Path('test')


@pytest.fixture()
def gut_settings(test_dir_path) -> GutSettings:
    GutSettings.GUT_DIR_PATH = test_dir_path / ".gut"
    gut_settings = GutSettings()
    return gut_settings
