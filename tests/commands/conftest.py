import hashlib
from pathlib import Path
import shutil

import pytest


@pytest.fixture()
def test_folder_path(test_dir_path) -> Path:
    return test_dir_path / "folder"


@pytest.fixture()
def test_folded_file_path(test_folder_path) -> Path:
    return test_folder_path / "folded_kek"


@pytest.fixture()
def test_file_path(test_dir_path) -> Path:
    return test_dir_path / "kek"


@pytest.fixture(autouse=True)
def prepare_test_dir(gut_settings, test_dir_path, test_folder_path, test_folded_file_path, test_file_path):
    test_dir_path.mkdir()

    gut_settings.objects_dir_path.mkdir(exist_ok=True, parents=True)
    gut_settings.heads_dir_path.mkdir(exist_ok=True, parents=True)

    gut_settings.index_file_path.touch(exist_ok=True)
    gut_settings.head_file_path.touch(exist_ok=True)

    gut_settings.default_head_file_path.touch(exist_ok=True)
    gut_settings.head_file_path.write_text(str(gut_settings.default_head_file_path))

    test_folder_path.mkdir()
    test_file_path.touch()
    test_folded_file_path.touch()

    yield

    shutil.rmtree(test_dir_path)


def hash_content(content: str) -> str:
    return hashlib.sha1(content.encode()).hexdigest()
