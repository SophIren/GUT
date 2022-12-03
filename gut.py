import argparse
from enum import Enum
from pathlib import Path

from typing import Dict, Callable

from command_handlers import InitHandler, AddHandler, StatusHandler


class Command(str, Enum):
    init = "init"
    add = "add"
    status = "status"
    commit = "commit"
    reset = "reset"

    def __str__(self) -> str:
        return self.value


class ArgHandler:
    @staticmethod
    def init(params: argparse.Namespace) -> None:
        InitHandler.handle()

    @staticmethod
    def add(params: argparse.Namespace) -> None:
        AddHandler().handle(Path(params.filename))

    @staticmethod
    def status(params: argparse.Namespace) -> None:
        StatusHandler().handle()


command_to_handler: Dict[Command, Callable[[argparse.Namespace], None]] = {
    Command.init: ArgHandler.init,
    Command.add: ArgHandler.add,
    Command.status: ArgHandler.status
}

parser = argparse.ArgumentParser(description='GUT VCS')
subparsers = parser.add_subparsers(help="gut command", dest="command_name")

init_parser = subparsers.add_parser(Command.init, help="gut initialization")

add_parser = subparsers.add_parser(Command.add, help="gut adding to track")
add_parser.add_argument("filename", type=str)

status_parser = subparsers.add_parser(Command.status, help="very gut status")

args = parser.parse_args()
command = Command(args.command_name)
command_to_handler[command](args)
