from enum import Enum
from itertools import count
from typing import List, Tuple, Iterator

from common import line_iterator, Pos, Direction


class Tile(Enum):
    AIR = False
    ROCK = True
    SAND = True

    def __init__(self, solid):
        self._s = solid

    @property
    def solid(self) -> bool:
        return self._s


class Grid:
    def __init__(self, width: int, height: int, offset_x: int, offset_y: int):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.grid: List[List[Tile]] = [[Tile.AIR for _ in range(width)] for _ in range(height)]

    def get_tile(self, pos: Pos) -> Tile:
        return self.grid[pos.y - self.offset_y][pos.x - self.offset_x]

    def set_tile(self, pos: Pos, tile: Tile):
        self.grid[pos.y - self.offset_y][pos.x - self.offset_x] = tile

    def is_in_bounds(self, pos: Pos) -> bool:
        return self.offset_x <= pos.x < self.offset_x + self.width and\
            self.offset_y <= pos.y < self.offset_y + self.height

    def can_place_sand(self, pos: Pos) -> bool:
        return self.is_in_bounds(pos) and not self.get_tile(pos).solid

    def draw_rock(self, from_pos: Pos, to_pos: Pos):
        if from_pos.y == to_pos.y:
            # draw horizontal line
            for x in range_between(from_pos.x, to_pos.x):
                self.set_tile(Pos(x, to_pos.y), Tile.ROCK)
        elif from_pos.x == to_pos.x:
            # draw vertical line
            for y in range_between(from_pos.y, to_pos.y):
                self.set_tile(Pos(to_pos.x, y), Tile.ROCK)
        else:
            raise RuntimeError('Diagonal lines are not supported')

    def drop_sand(self, sand_pos: Pos) -> Tuple[Pos, bool]:
        while True:
            rest = True
            for c_pos in sand_fall_options(sand_pos):
                if not self.is_in_bounds(c_pos):
                    return c_pos, False
                if not self.get_tile(c_pos).solid:
                    sand_pos = c_pos
                    rest = False
                    break
            if rest:
                self.set_tile(sand_pos, Tile.SAND)
                return sand_pos, True


def range_between(num1: int, num2: int) -> range:
    return range(min(num1, num2), max(num1, num2) + 1, 1)


def sand_fall_options(current_pos: Pos) -> Iterator[Pos]:
    current_pos += Direction.Down
    yield current_pos
    yield current_pos + Direction.Left
    yield current_pos + Direction.Right


def read_input(input_str: str, start_point: Pos, prt2: bool) -> Grid:
    line_def_ls: List[List[Pos]] = []
    all_points: List[Pos] = [start_point]
    for line in line_iterator(input_str):
        pl = [Pos(int(p[0].strip()), int(p[1].strip())) for p in (ps.strip().split(',') for ps in line.split('->'))]
        line_def_ls.append(pl)
        all_points.extend(pl)
    minx = min((p.x for p in all_points))
    maxx = max((p.x for p in all_points))
    miny = min((p.y for p in all_points))
    maxy = max((p.y for p in all_points))

    if prt2:  # part 2
        maxy += 2
        h = 1 + maxy - miny
        minx = min(minx, start_point.x - h + 1)
        maxx = max(maxx, start_point.x + h - 1)

    grid = Grid(width=1+maxx-minx, height=1+maxy-miny, offset_x=minx, offset_y=miny)
    for ld in line_def_ls:
        for p1, p2 in zip(ld, ld[1:]):
            grid.draw_rock(p1, p2)
    if prt2:
        grid.draw_rock(Pos(x=minx, y=maxy), Pos(x=maxx, y=maxy))
    return grid


def d14p1_solution(input_str: str) -> str:
    start_point = Pos(500, 0)
    grid = read_input(input_str, start_point=start_point, prt2=False)

    sand_dropped = None
    for sand_dropped in count():
        _, resting = grid.drop_sand(start_point)
        if not resting:
            break

    return str(sand_dropped)


def d14p2_solution(input_str: str) -> str:
    start_point = Pos(500, 0)
    grid = read_input(input_str, start_point=start_point, prt2=True)

    sand_dropped = None
    for sand_dropped in count(1):
        sand_pos, resting = grid.drop_sand(start_point)
        if not resting:
            raise RuntimeError('Something went wrong: sand fell into abyss in part 2')
        if sand_pos == start_point:
            break

    return str(sand_dropped)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=14, part=1)
    run_puzzle(day=14, part=2)
