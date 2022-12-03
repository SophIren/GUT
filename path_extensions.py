from pathlib import Path
from typing import Callable, Iterable


def apply_func_to_batches(file_path: Path, func: Callable, buffer_size: int = 65536) -> Iterable:
    with file_path.open(mode='rb') as file:
        while True:
            data = file.read(buffer_size)
            if not data:
                break
            yield func(data)
