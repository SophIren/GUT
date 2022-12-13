import pytest

from handlers import CommitHandler
from handlers.commands import AddHandler
from tests.commands.conftest import hash_content


@pytest.mark.parametrize("commit_message", ["kek", "lol"])
def test_commit_folded_file(gut_settings, test_folded_file_path, commit_message):
    AddHandler().handle(test_folded_file_path)
    CommitHandler().handle(test_folded_file_path, commit_message)

    files = set(path.name for path in gut_settings.objects_dir_path.glob('*'))

    expected_file_content_hash = hash_content(test_folded_file_path.read_text())
    expected_dir_content_hash = hash_content(f"blob {expected_file_content_hash} {str(test_folded_file_path)}")
    expected_dir_hash = hash_content(f"tree {expected_dir_content_hash} {str(test_folded_file_path.parent)}")
    expected_commit_hash = hash_content(f"parent \ntree {expected_dir_hash}\n\n{commit_message}")

    assert files == {expected_dir_hash, expected_dir_content_hash, expected_file_content_hash, expected_commit_hash}


@pytest.mark.parametrize("commit_message", ["kek", "lol"])
def test_commit_folder(gut_settings, test_folder_path, commit_message):
    AddHandler().handle(test_folder_path)
    CommitHandler().handle(test_folder_path, commit_message)

    files = set(path.name for path in gut_settings.objects_dir_path.glob('*'))

    expected = set()
    expected_folder_lines = []
    for file in test_folder_path.glob('*'):
        expected_file_content_hash = hash_content(file.read_text())
        expected.add(expected_file_content_hash)
        expected_folder_lines.append(f"blob {expected_file_content_hash} {str(file)}")
    expected_dir_content_hash = hash_content('\n'.join(expected_folder_lines))
    expected_dir_hash = hash_content(f"tree {expected_dir_content_hash} {str(test_folder_path)}")
    expected_commit_hash = hash_content(f"parent \ntree {expected_dir_hash}\n\n{commit_message}")
    expected.add(expected_dir_hash)
    expected.add(expected_commit_hash)
    expected.add(expected_dir_content_hash)

    assert expected == files
