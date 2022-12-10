from handlers.common import CommonHandler


class InitHandler(CommonHandler):
    @classmethod
    def handle(cls) -> None:
        cls.settings.OBJECTS_DIR_PATH.mkdir(exist_ok=True, parents=True)
        cls.settings.HEADS_DIR_PATH.mkdir(exist_ok=True, parents=True)

        cls.settings.INDEX_FILE_PATH.touch(exist_ok=True)
        cls.settings.HEAD_FILE_PATH.touch(exist_ok=True)

        cls.settings.DEFAULT_HEAD_FILE_PATH.touch(exist_ok=True)
        cls.settings.HEAD_FILE_PATH.write_text(str(cls.settings.DEFAULT_HEAD_FILE_PATH))
