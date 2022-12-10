from handlers.index_handler import IndexHandler


class InitHandler(IndexHandler):
    @classmethod
    def handle(cls) -> None:
        cls.OBJECTS_DIR_PATH.mkdir(exist_ok=True, parents=True)
        cls.HEADS_DIR_PATH.mkdir(exist_ok=True, parents=True)

        cls.INDEX_FILE_PATH.touch(exist_ok=True)
        cls.HEAD_FILE_PATH.touch(exist_ok=True)

        cls.DEFAULT_HEAD_FILE_PATH.touch(exist_ok=True)
        cls.HEAD_FILE_PATH.write_text(str(cls.DEFAULT_HEAD_FILE_PATH))
