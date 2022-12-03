import itertools
from typing import List

from common import line_iterator


def parse_elves(input_str: str) -> List[int]:
    elves: List[int] = []
    current_elf = 0
    for line in itertools.chain(line_iterator(input_str), ['']):
        line = line.strip()
        if line:
            current_elf += int(line)
            continue
        elves.append(current_elf)
        current_elf = 0
    return elves


def d1p1_solution(input_str: str) -> str:
    return str(max(parse_elves(input_str)))


def d1p2_solution(input_str: str) -> str:
    elves = parse_elves(input_str)
    if len(elves) < 3:
        raise RuntimeError('Invalid input')
    return str(sum(sorted(elves, reverse=True)[:3]))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=1, part=1)
    run_puzzle(day=1, part=2)
