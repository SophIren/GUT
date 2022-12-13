from pathlib import Path
from typing import Set

from gut_settings import GutSettings


class GutignoreHandler(GutSettings):  # ToDo: Не наследовать от настроек?
    def __init__(self):  # Todo: сделать чтобы подходило под руглярки
        super().__init__()
        self.gutignore = self.read_gutignore()

    def read_gutignore(self) -> Set[Path]:
        if not self.gutignore_file_path.exists():
            return set()
        res = {self.gutignore_file_path, self.GUT_DIR_PATH}
        with self.gutignore_file_path.open(mode='r') as gutignore_file:
            for line in gutignore_file.readlines():
                res.add(Path(line.strip()))
        return res
