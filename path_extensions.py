from pathlib import Path
from typing import Callable


def apply_func_to_batches(file_path: Path, func: Callable, buffer_size: int = 65536) -> None:
    with file_path.open(mode='rb') as file:
        while True:
            data = file.read(buffer_size)
            if not data:
                break
            func(data)
