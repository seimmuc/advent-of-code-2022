import math
import re
import time
from collections import deque
from itertools import chain
from typing import Callable, Optional, Deque, List, Any, Dict

from common import line_iterator


monkey_line_regex = re.compile(r'Monkey (\d+):')

operation_regex = re.compile(r'new = (old|\d+) ([+\-*]) (old|\d+)')
test_regex = re.compile(r'divisible by (\d+)')
throw_regex = re.compile(r'throw to monkey (\d+)')

indent = '  '
k_starting_items = 'Starting items:'
k_operation = 'Operation:'
k_test = 'Test:'
k_if_true = indent + 'If true:'
k_if_false = indent + 'If false:'


class Monkey:
    def __init__(self, starting_items: List[int], operation: 'Operation', test: 'Test', if_true: int, if_false: int):
        self.items: Deque[int] = deque(i for i in starting_items)
        self.operation: Operation = operation
        self.test: Test = test
        self.targets = {True: if_true, False: if_false}

        self.inspection_count = 0

    @staticmethod
    def parse_line(line: str, d: Dict[str, Any]):
        if line.startswith(k_starting_items):
            d['si'] = [int(wls) for wls in line[len(k_starting_items):].strip().split(', ')]
        elif line.startswith(k_operation):
            d['op'] = Operation.from_str(line[len(k_operation):])
        elif line.startswith(k_test):
            d['ts'] = Test.from_str(line[len(k_test):])
        elif line.startswith(k_if_true):
            d['it'] = int(throw_regex.match(line[len(k_if_true):].strip())[1])
        elif line.startswith(k_if_false):
            d['if'] = int(throw_regex.match(line[len(k_if_false):].strip())[1])
        else:
            raise RuntimeError(f'Invalid monkey entry: {line}')

    @classmethod
    def from_lines(cls, lines: List[str]):
        d = {}
        for line in lines:
            cls.parse_line(line, d)
        return cls(starting_items=d['si'], operation=d['op'], test=d['ts'], if_true=d['it'], if_false=d['if'])

    def play_turn(self, monkeys: List['Monkey'], relief_factor: int, lcm: Optional[int]):
        while self.items:
            worry_level = self.items.popleft()

            # inspect
            worry_level = self.operation.perform(worry_level)

            # relief / optimisation
            worry_level //= relief_factor
            if lcm:
                worry_level %= lcm

            # test
            test_result = self.test.test(worry_level)

            # throw
            target_id = self.targets[test_result]
            monkeys[target_id].items.append(worry_level)

            # monkeys are well known for their record keeping
            self.inspection_count += 1


class Operation:
    operations = {'+': int.__add__, '*': int.__mul__}

    def __init__(self, operator: Callable[[int, int], int], l_val: Optional[int], r_val: Optional[int]):
        self.operator = operator
        self.l_val = l_val
        self.r_val = r_val

    def perform(self, old_val: int) -> int:
        l = old_val if self.l_val is None else self.l_val
        r = old_val if self.r_val is None else self.r_val
        return self.operator(l, r)

    @classmethod
    def from_str(cls, operation_str: str) -> 'Operation':
        match = operation_regex.match(operation_str.strip())
        lv, op, rv = match[1], match[2], match[3]
        op = cls.operations[op]
        lv = None if lv == 'old' else int(lv)
        rv = None if rv == 'old' else int(rv)
        return cls(operator=op, l_val=lv, r_val=rv)


class Test:
    def __init__(self, divisible_by: int):
        self.divisible_by = divisible_by

    def test(self, worry_level: int) -> bool:
        return worry_level % self.divisible_by == 0

    @classmethod
    def from_str(cls, test_str: str):
        match = test_regex.match(test_str.strip())
        return cls(divisible_by=int(match[1]))


def play_round(monkeys: List[Monkey], relief_factor: int, lcm: Optional[int] = None):
    for monkey in monkeys:
        monkey.play_turn(monkeys=monkeys, relief_factor=relief_factor, lcm=lcm)


def read_input(input_str: str) -> List[Monkey]:
    monkeys: List[Monkey] = []
    current_monkey_lines: Optional[List[str]] = None
    for line in chain(line_iterator(input_str), ['']):
        if not line.strip():
            m = Monkey.from_lines(current_monkey_lines)
            m_id = len(monkeys)
            if m_id in m.targets.values():
                raise RuntimeError(f'Monkey {m_id} targets itself')
            monkeys.append(m)
            current_monkey_lines = None
        elif current_monkey_lines is None:
            match = monkey_line_regex.match(line)
            if int(match[1]) != len(monkeys):
                raise RuntimeError(f'Out of order monkeys: expected {len(monkeys)}, got "{match[1]}"')
            current_monkey_lines = []
        elif line.startswith(indent):
            current_monkey_lines.append(line[len(indent):])
        else:
            raise RuntimeError(f'Unexpected line: "{line}"')
    return monkeys


def d11p1_solution(input_str: str) -> str:
    monkeys = read_input(input_str)
    for _ in range(20):
        play_round(monkeys=monkeys, relief_factor=3)
    monkey_business = int.__mul__(*sorted(m.inspection_count for m in monkeys)[-2:])
    return str(monkey_business)


def d11p2_solution(input_str: str) -> str:
    monkeys = read_input(input_str)
    lcm = 1     # Lowest common multiple
    for m in monkeys:
        lcm = abs(lcm * m.test.divisible_by) // math.gcd(lcm, m.test.divisible_by)
    for i in range(10000):
        play_round(monkeys=monkeys, relief_factor=1, lcm=lcm)
    monkey_business = int.__mul__(*sorted(m.inspection_count for m in monkeys)[-2:])
    return str(monkey_business)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=11, part=1)
    run_puzzle(day=11, part=2)
