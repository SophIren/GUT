from pathlib import Path
from typing import Set

from gut_settings import GutSettings


class GutignoreHandler(GutSettings):  # ToDo: Не наследовать от настроек?
    def __init__(self):  # Todo: сделать чтобы подходило под руглярки
        self.gutignore = self.read_gutignore()

    @classmethod
    def read_gutignore(cls) -> Set[Path]:  # ToDo check if .gutignore doesn't exist
        res = {cls.GUTIGNORE_FILE_PATH, cls.GUT_DIR_PATH}
        with cls.GUTIGNORE_FILE_PATH.open(mode='r') as gutignore_file:
            for line in gutignore_file.readlines():
                res.add(Path(line.strip()))
        return res
