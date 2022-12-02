from command_handlers.common import CommonHandler


class StatusHandler(CommonHandler):
    @classmethod
    def handle(cls) -> None:
        index = cls.read_index()
        print(index)
