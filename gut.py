import argparse
from enum import Enum
from pathlib import Path

from typing import Dict, Callable

from command_handlers import InitHandler, AddHandler, StatusHandler, CommitHandler
from command_handlers.branch import BranchHandler


class Command(str, Enum):
    init = "init"
    add = "add"
    status = "status"
    commit = "commit"
    reset = "reset"
    branch = "branch"

    def __str__(self) -> str:
        return self.value


class ArgHandler:
    @staticmethod
    def init(params: argparse.Namespace) -> None:
        InitHandler.handle()

    @staticmethod
    def add(params: argparse.Namespace) -> None:
        AddHandler().handle(Path(params.path))

    @staticmethod
    def status(params: argparse.Namespace) -> None:
        StatusHandler().handle()

    @staticmethod
    def commit(params: argparse.Namespace) -> None:
        CommitHandler().handle(Path(params.path), params.message)

    @staticmethod
    def branch(params: argparse.Namespace) -> None:
        BranchHandler().handle(
            switch_to=params.switch, rename_to=params.rename, delete_name=params.delete
        )


command_to_handler: Dict[Command, Callable[[argparse.Namespace], None]] = {
    Command.init: ArgHandler.init,
    Command.add: ArgHandler.add,
    Command.status: ArgHandler.status,
    Command.commit: ArgHandler.commit,
    Command.branch: ArgHandler.branch
}

parser = argparse.ArgumentParser(description='GUT VCS')
subparsers = parser.add_subparsers(help="gut command", dest="command_name")

init_parser = subparsers.add_parser(Command.init, help="gut initialization")

add_parser = subparsers.add_parser(Command.add, help="gut adding to track")
add_parser.add_argument("path", type=str)

status_parser = subparsers.add_parser(Command.status, help="very gut status")

commit_parser = subparsers.add_parser(Command.commit, help="Very gut commit chmod")
commit_parser.add_argument("path", type=str)
commit_parser.add_argument("message", type=str)

branch_parser = subparsers.add_parser(Command.branch, help="gut branches")
branch_parser.add_argument("switch", type=str, nargs='?')
branch_parser.add_argument("-c", "--create", type=str)
branch_parser.add_argument("-d", "--delete", type=str)
branch_parser.add_argument("-r", "--rename", type=str)

args = parser.parse_args()
command = Command(args.command_name)
command_to_handler[command](args)
