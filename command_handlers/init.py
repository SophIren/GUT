from command_handlers.common import CommonHandler


class InitHandler(CommonHandler):
    @classmethod
    def handle(cls) -> None:
        cls.settings.OBJECTS_DIR_PATH.mkdir(parents=True, exist_ok=True)
        cls.settings.INDEX_FILE_PATH.touch(exist_ok=True)
        cls.settings.HEAD_FILE_PATH.touch(exist_ok=True)
