from collections import deque
from typing import List, Tuple, NamedTuple, Optional, Dict, Deque, Iterator

from common import line_iterator, Direction, Pos


class HeightMap:
    def __init__(self, grid: List[List[int]], width: int, height: int):
        self.grid = grid
        self.width = width
        self.height = height

    def get_height(self, pos: Pos) -> int:
        return self.grid[pos.y][pos.x]

    def in_bounds(self, pos: Pos) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def can_move(self, from_pos: Pos, direction: Direction):
        to_pos = from_pos + direction
        return self.in_bounds(to_pos) and self.get_height(to_pos) <= self.get_height(from_pos) + 1

    def scan_all_positions(self) -> Iterator[Pos]:
        for y in range(self.height):
            for x in range(self.width):
                yield Pos(x, y)


class PathNode(NamedTuple):
    step_num: int
    pos: Pos
    step_dir: Optional[Direction]


class Path:
    def __init__(self, nodes: List[PathNode]):
        self.nodes = nodes

    @property
    def last_step(self):
        return self.nodes[-1]

    def step_in(self, direction: Direction) -> 'Path':
        next_step = PathNode(self.last_step.step_num + 1, self.last_step.pos + direction, direction)
        return Path(self.nodes + [next_step])


def solve(height_map: HeightMap, start_pos: Pos, end_pos: Pos) -> Optional[Path]:
    # this algorithm can be optimized to significantly reduce memory usage
    start_path = Path([PathNode(step_num=0, pos=start_pos, step_dir=None)])
    locations: Dict[Pos, Path] = {start_pos: start_path}
    last_steps: Deque[Path] = deque((start_path,))
    while last_steps:
        new_steps: Deque[Path] = deque()
        while last_steps:
            path = last_steps.popleft()
            path_pos = path.last_step.pos
            for d in Direction:
                if not height_map.can_move(path_pos, d):
                    continue
                if path_pos + d not in locations:
                    new_path = path.step_in(d)
                    if new_path.last_step.pos == end_pos:
                        return new_path
                    locations[new_path.last_step.pos] = new_path
                    new_steps.append(new_path)
        last_steps = new_steps
    return None


def read_input(input_str: str) -> Tuple[HeightMap, Pos, Pos]:
    start_pos = None
    end_pos = None
    width = None
    grid: List[List[int]] = []
    for y, line in enumerate(line_iterator(input_str)):
        if width is None:
            width = len(line)
        elif len(line) != width:
            raise RuntimeError('Inconsistent map width')
        if 'S' in line:
            start_pos = Pos(line.index('S'), y)
            line = line.replace('S', 'a')
        if 'E' in line:
            end_pos = Pos(line.index('E'), y)
            line = line.replace('E', 'z')
        row = []
        for c in line:
            h = ord(c) - 97
            if not 0 <= h <= 25:
                raise RuntimeError(f'Invalid height: "{c}" in line {y + 1}')
            row.append(h)
        grid.append(row)
    if start_pos is None or end_pos is None:
        raise RuntimeError('Missing start or end position')
    return HeightMap(grid=grid, width=width, height=len(grid)), start_pos, end_pos


def d12p1_solution(input_str: str) -> str:
    height_map, start_pos, end_pos = read_input(input_str)
    solution = solve(height_map=height_map, start_pos=start_pos, end_pos=end_pos)
    if solution is None:
        raise RuntimeError('No solution was found')
    return str(solution.last_step.step_num)


def d12p2_solution(input_str: str) -> str:
    # this could be optimised by running pathfinder backwards and treating any height=0 as solution
    height_map, _, end_pos = read_input(input_str)
    lowest_elevations = [s for s in height_map.scan_all_positions() if height_map.get_height(s) == 0]
    best_trail: Optional[Path] = None
    for start in lowest_elevations:
        solution = solve(height_map=height_map, start_pos=start, end_pos=end_pos)
        if solution is not None:
            if best_trail is None or solution.last_step.step_num < best_trail.last_step.step_num:
                best_trail = solution
    if best_trail is None:
        raise RuntimeError('No trails are possible')
    return str(best_trail.last_step.step_num)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=12, part=1)
    run_puzzle(day=12, part=2)
