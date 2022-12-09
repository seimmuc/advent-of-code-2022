from enum import Enum
from typing import List, Iterator, Tuple, Set, Optional

from common import line_iterator


class Direction(Enum):
    U = (0, -1)
    D = (0, 1)
    L = (-1, 0)
    R = (1, 0)


class Move:
    __slots__ = ['direction', 'distance']

    def __init__(self, direction: Direction, distance: int):
        self.direction = direction
        self.distance = distance

    def __repr__(self) -> str:
        return f'Move({self.direction.name, self.distance})'


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


def clamp_offset(offset: int) -> int:
    if offset > 1:
        return 1
    if offset < -1:
        return -1
    return 0


class Knot:
    def __init__(self, child: Optional['Knot'], pos: Pos):
        self.child = child
        self.pos = pos

    def update_child(self):
        c = self.child
        if c is None:
            return
        offset_x, offset_y = self.pos - c.pos
        if abs(offset_x) > 1 or abs(offset_y) > 1:
            c.pos = Pos(self.pos.x - clamp_offset(offset_x), self.pos.y - clamp_offset(offset_y))


class State:
    def __init__(self, start: Pos, knot_count: int):
        if knot_count < 1:
            raise RuntimeError('must have at least one knot')
        self.knots = []
        for _ in range(knot_count):
            self.knots.append(Knot(child=(self.tail if self.knots else None), pos=start))
        self.knots.reverse()

    @property
    def head(self) -> Knot:
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    def step_iter(self, move: Move) -> Iterator[None]:
        for i in range(move.distance):
            self.head.pos += move.direction
            for knot in self.knots:
                knot.update_child()
            yield


def read_input(input_str: str) -> List[Move]:
    moves: List[Move] = []
    for line in line_iterator(input_str):
        dr, dist = line.split(' ', maxsplit=1)
        moves.append(Move(Direction[dr], int(dist)))
    return moves


def d9p1_solution(input_str: str) -> str:
    moves = read_input(input_str)
    state = State(Pos(0, 0), 2)
    unique_tail_positions: Set[Pos] = set()
    for move in moves:
        for _ in state.step_iter(move):
            unique_tail_positions.add(state.tail.pos)
    return str(len(unique_tail_positions))


def d9p2_solution(input_str: str) -> str:
    moves = read_input(input_str)
    state = State(Pos(0, 0), 10)
    unique_tail_positions: Set[Pos] = set()
    for move in moves:
        for _ in state.step_iter(move):
            unique_tail_positions.add(state.tail.pos)
    return str(len(unique_tail_positions))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=9, part=1)
    run_puzzle(day=9, part=2)
