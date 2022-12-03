from command_handlers.common import CommonHandler


class InitHandler(CommonHandler):
    @classmethod
    def handle(cls) -> None:
        cls.settings.OBJECTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.settings.INDEX_FILE.touch(exist_ok=True)
