from command_handlers.common import CommonHandler


class StatusHandler(CommonHandler):
    def handle(self) -> None:
        print(self.index)
