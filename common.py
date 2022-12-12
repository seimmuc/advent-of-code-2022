from abc import ABC, abstractmethod
from enum import Enum
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Callable, Iterator, Union, Tuple


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


# 2D grids

class Direction(Enum):
    Up = (0, -1)
    Down = (0, 1)
    Left = (-1, 0)
    Right = (1, 0)


class Pos:
    __slots__ = ['x', 'y']

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, direction: Direction) -> 'Pos':
        return Pos(self.x + direction.value[0], self.y + direction.value[1])

    def __sub__(self, other: 'Pos') -> Tuple[int, int]:
        return self.x - other.x, self.y - other.y

    def __repr__(self):
        return f'Pos({self.x}, {self.y})'

    def __eq__(self, other: 'Pos'):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
