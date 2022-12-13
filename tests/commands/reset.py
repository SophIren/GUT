from handlers import CommitHandler
from handlers.commands import AddHandler
from handlers.commands.reset import ResetHandler
from tests.commands.conftest import hash_content


def test_reset(gut_settings, test_folder_path):
    AddHandler().handle(test_folder_path)
    first_commit_handler = CommitHandler()
    first_commit_handler.handle(test_folder_path, "1st")

    expected = set()
    folder_lines = []
    for file in test_folder_path.glob('*'):
        expected_file_content_hash = hash_content(file.read_text())
        expected.add(expected_file_content_hash)
        folder_lines.append(f"blob {expected_file_content_hash} {str(file)}")
    dir_content_hash = hash_content('\n'.join(folder_lines))
    dir_hash = hash_content(f"tree {dir_content_hash} {str(test_folder_path)}")
    first_commit_hash = hash_content(f"parent \ntree {dir_hash}\n\n1st")

    next(test_folder_path.glob('*')).write_text("kek")
    new_file = test_folder_path / 'hehe.txt'
    new_file.touch()
    new_file.write_text("lol")
    AddHandler().handle(test_folder_path)
    CommitHandler().handle(test_folder_path, "2nd")

    reset_handler = ResetHandler()
    reset_handler.handle(first_commit_hash)

    for obj in reset_handler.index:
        assert reset_handler.index[obj].stage_hash == first_commit_handler.index[obj].stage_hash
