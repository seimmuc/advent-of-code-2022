from abc import ABC, abstractmethod
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Callable, Iterator, Union


PuzzleSolution = Callable[[str], str]


class Solution(ABC):
    @staticmethod
    @abstractmethod
    def solve(puzzle_input: str):
        raise NotImplemented


def line_iterator(multiline_string: str, strip_newline: bool = True) -> Iterator[str]:
    for line in StringIO(multiline_string):
        if strip_newline:
            line = line.rstrip('\r\n')
        yield line


def load_input_from_file(path: Union[Path, str]) -> str:
    if not isinstance(path, PathLike):
        path = Path(path)
    with open(path, mode='rt', encoding='utf8', newline='\n') as f:
        return f.read()
