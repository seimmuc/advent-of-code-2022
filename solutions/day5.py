import re
from collections import deque
from dataclasses import dataclass
from typing import Tuple, List, Deque

from common import line_iterator


stack_legend_regex = re.compile(r'\n( +(?:\d{1,3} *)+)\n\n')
crate_regex = re.compile(r'\[([A-Z])]')
move_regex = re.compile(r'move (\d+) from (\d+) to (\d+)')


@dataclass
class Move:
    crate_num: int
    from_stack: int
    to_stack: int


def split_input_parts(input_str: str) -> Tuple[str, str, int]:
    match = stack_legend_regex.search(input_str)
    crates = input_str[:match.start()]
    stack_nums = match[1].split()
    moves = input_str[match.end():]
    stack_count = len(stack_nums)
    if int(stack_nums[-1].strip()) != stack_count:
        raise RuntimeError()
    return crates, moves, stack_count


def read_crates(crates_str: str, stack_count: int) -> List[Deque[str]]:
    crates: List[Deque[str]] = [deque() for _ in range(stack_count)]
    for line in line_iterator(crates_str):
        for i in range(stack_count):
            p = i * 4
            if p > len(line):
                break
            cm = crate_regex.match(line[p:p+3])
            if cm is None:
                continue
            crates[i].appendleft(cm[1])
    return crates


def read_moves(moves_str: str, stack_count: int) -> List[Move]:
    moves: List[Move] = []
    sr = range(stack_count)
    for line in line_iterator(moves_str):
        match = move_regex.match(line)
        move = Move(crate_num=int(match[1]), from_stack=int(match[2])-1, to_stack=int(match[3])-1)
        if move.from_stack not in sr or move.to_stack not in sr or move.from_stack == move.to_stack:
            raise RuntimeError()
        moves.append(move)
    return moves


def read_all(input_str: str) -> Tuple[List[Deque[str]], List[Move]]:
    cs, ms, stack_count = split_input_parts(input_str)
    crates = read_crates(cs, stack_count)
    moves = read_moves(ms, stack_count)
    return crates, moves


def execute_moves_9000(crates: List[Deque[str]], moves: List[Move]):
    for move in moves:
        for _ in range(move.crate_num):
            load: str = crates[move.from_stack].pop()
            crates[move.to_stack].append(load)


def execute_moves_9001(crates: List[Deque[str]], moves: List[Move]):
    for move in moves:
        fs = crates[move.from_stack]
        load: List[str] = list(fs.pop() for _ in range(move.crate_num))
        crates[move.to_stack].extend(reversed(load))


def d5p1_solution(input_str: str) -> str:
    crates, moves = read_all(input_str)
    execute_moves_9000(crates, moves)
    return ''.join(c[-1] for c in crates)


def d5p2_solution(input_str: str) -> str:
    crates, moves = read_all(input_str)
    execute_moves_9001(crates, moves)
    return ''.join(c[-1] for c in crates)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=5, part=1)
    run_puzzle(day=5, part=2)
