import argparse
from enum import Enum
from pathlib import Path

from typing import Dict, Callable

from handlers.commands import InitHandler, AddHandler, StatusHandler, CommitHandler, BranchHandler
from handlers.commands.log import LogHandler
from handlers.commands.reset import ResetHandler
from handlers.commands.squash import SquashHandler


class Command(str, Enum):
    init = "init"
    add = "add"
    status = "status"
    commit = "commit"
    reset = "reset"
    branch = "branch"
    log = "log"
    squash = "squash"

    def __str__(self) -> str:
        return self.value


class ArgHandler:
    @staticmethod
    def init(params: argparse.Namespace) -> None:
        InitHandler().handle()

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
            switch_to=params.checkout,
            create_name=params.create,
            rename_to_name=params.rename,
            delete_name=params.delete
        )

    @staticmethod
    def reset(params: argparse.Namespace) -> None:
        ResetHandler().handle(to_commit=params.commit)

    @staticmethod
    def log(params: argparse.Namespace) -> None:
        LogHandler().handle()

    @staticmethod
    def squash(params: argparse.Namespace) -> None:
        SquashHandler().handle(params.lower, params.upper)


command_to_handler: Dict[Command, Callable[[argparse.Namespace], None]] = {
    Command.init: ArgHandler.init,
    Command.add: ArgHandler.add,
    Command.status: ArgHandler.status,
    Command.commit: ArgHandler.commit,
    Command.branch: ArgHandler.branch,
    Command.reset: ArgHandler.reset,
    Command.log: ArgHandler.log,
    Command.squash: ArgHandler.squash
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
branch_parser.add_argument("checkout", type=str, nargs='?')
branch_parser.add_argument("-c", "--create", type=str)
branch_parser.add_argument("-d", "--delete", type=str)
branch_parser.add_argument("-r", "--rename", type=str)

reset_parser = subparsers.add_parser(Command.reset, help="reset gutly")
reset_parser.add_argument("commit", type=str)

log_parser = subparsers.add_parser(Command.log, help="gut log")

squash_parser = subparsers.add_parser(Command.squash, help="gut help")
squash_parser.add_argument("lower", type=str, help="lower commit")
squash_parser.add_argument("upper", type=str, help="upper commit")

args = parser.parse_args()
command = Command(args.command_name)
command_to_handler[command](args)
