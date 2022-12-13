from handlers.commands import AddHandler
from tests.commands.conftest import hash_content


def test_add_folded_file(gut_settings, test_folded_file_path):
    AddHandler().handle(test_folded_file_path)

    files = set(path.name for path in gut_settings.objects_dir_path.glob('*'))

    expected_file_content_hash = hash_content(test_folded_file_path.read_text())
    expected_dir_content_hash = hash_content(f"blob {expected_file_content_hash} {str(test_folded_file_path)}")
    assert files == {expected_dir_content_hash, expected_file_content_hash}


def test_add_folder(gut_settings, test_folder_path):
    AddHandler().handle(test_folder_path)

    files = set(path.name for path in gut_settings.objects_dir_path.glob('*'))

    expected = set()
    expected_folder_lines = []
    for file in test_folder_path.glob('*'):
        expected_file_content_hash = hash_content(file.read_text())
        expected.add(expected_file_content_hash)
        expected_folder_lines.append(f"blob {expected_file_content_hash} {str(file)}")
    expected_dir_content_hash = hash_content('\n'.join(expected_folder_lines))
    expected.add(expected_dir_content_hash)

    assert files == expected
