from handlers.commands import InitHandler

import shutil


def test_init(test_dir_path):
    init_handler = InitHandler()
    gut_dir_path = test_dir_path / init_handler.GUT_DIR_PATH
    init_handler.GUT_DIR_PATH = gut_dir_path
    init_handler.handle()

    assert gut_dir_path.exists()
    assert init_handler.objects_dir_path.exists()
    assert init_handler.head_file_path.exists()
    assert init_handler.heads_dir_path.exists()

    shutil.rmtree(test_dir_path)
