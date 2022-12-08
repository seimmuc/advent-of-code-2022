from enum import Enum
from typing import List, Tuple, Optional

from common import line_iterator


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


class Grid:
    def __init__(self, grid: List[List[int]]):
        self.height = len(grid)
        if self.height < 1:
            raise RuntimeError('height cannot be zero')
        self.width = len(grid[0])
        if self.width < 1:
            raise RuntimeError('width cannot be zero')
        if sum(len(row) != self.width for row in grid) > 0:
            raise RuntimeError('inconsistent row width')
        self.grid = grid

    def get_tree(self, pos: Pos) -> int:
        return self.grid[pos.y][pos.x]

    def is_visible(self, pos: Pos) -> bool:
        for d in Direction:
            _, visible = self.look(from_pos=pos, direction=d)
            if visible:
                return True
        return False

    def in_bounds(self, pos: Pos) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def look(self, from_pos: Pos, direction: Direction) -> Tuple[List[int], bool]:
        # return: (list(tree_height), can_see_edge)
        res: List[int] = []
        p: Pos = from_pos
        th: int = self.get_tree(from_pos)
        while True:
            p += direction
            if not self.in_bounds(p):
                return res, True
            res.append(self.get_tree(p))
            if self.get_tree(p) >= th:
                return res, False


def read_input(input_str: str) -> Grid:
    g: List[List[int]] = []
    for line in line_iterator(input_str):
        g.append([int(c) for c in line])
    return Grid(grid=g)


def d8p1_solution(input_str: str) -> str:
    grid: Grid = read_input(input_str)
    visible_trees = 0
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.is_visible(Pos(x, y)):
                visible_trees += 1
    return str(visible_trees)


def d8p2_solution(input_str: str) -> str:
    grid: Grid = read_input(input_str)
    best_tree: Optional[Tuple[Pos, int]] = None
    for x in range(grid.width):
        for y in range(grid.height):
            score = 1
            p = Pos(x, y)
            for d in Direction:
                score *= len(grid.look(from_pos=p, direction=d)[0])
            if best_tree is None or best_tree[1] < score:
                best_tree = (p, score)
    return str(best_tree[1])


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=8, part=1)
    run_puzzle(day=8, part=2)
