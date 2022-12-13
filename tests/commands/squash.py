from handlers import CommitHandler
from handlers.commands import AddHandler
from handlers.commands.squash import SquashHandler
from tests.commands.conftest import hash_content


def test_squash(gut_settings, test_folder_path):
    AddHandler().handle(test_folder_path)
    commit_handler = CommitHandler()
    commit_handler.handle(test_folder_path, "1st")
    commit_handler.handle(test_folder_path, "2nd")
    commit_handler.handle(test_folder_path, "3rd")

    folder_lines = []
    for file in test_folder_path.glob('*'):
        expected_file_content_hash = hash_content(file.read_text())
        folder_lines.append(f"blob {expected_file_content_hash} {str(file)}")
    dir_content_hash = hash_content('\n'.join(folder_lines))
    dir_hash = hash_content(f"tree {dir_content_hash} {str(test_folder_path)}")

    lower_commit_hash = hash_content(f"parent \ntree {dir_hash}\n\n1st")
    second_commit_hash = hash_content(f"parent {lower_commit_hash}\ntree {dir_hash}\n\n2nd")
    upper_commit_hash = hash_content(f"parent {second_commit_hash}\ntree {dir_hash}\n\n3rd")
    SquashHandler().handle(lower_commit_hash, upper_commit_hash)

    with (gut_settings.objects_dir_path / upper_commit_hash).open() as obj_file:
        parent_line = obj_file.readline().split()
        if len(parent_line) == 2:
            _, parent = parent_line
        else:
            parent = ''

    assert parent == ''
