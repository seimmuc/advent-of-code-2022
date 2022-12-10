from abc import ABC, abstractmethod
from collections import deque
from itertools import count
from typing import List, Deque, Optional, Iterator

from common import line_iterator


class State:
    def __init__(self, instructions: Deque['Instruction']):
        self.cycle_num = 0
        self.output = 1     # register value during as it was during the last cycle
        self.register = 1   # register value that was set at the end of last cycle
        self.instructions = instructions
        self.current_instruction: Optional[Instruction] = None
        self.pi = None

    def execute_cycle(self) -> bool:
        if self.current_instruction is None:
            if not self.instructions:
                return False
            self.current_instruction = self.instructions.popleft()
        # from this point on, a cycle is guaranteed to run
        self.output = self.register
        result = self.current_instruction.run_cycle(state=self)
        if result is True:
            self.pi = self.current_instruction
            self.current_instruction = None
        self.cycle_num += 1
        return True

    def iter_cycles(self, cycle_count: Optional[int]) -> Iterator[int]:
        for _ in count(0) if cycle_count is None else range(cycle_count):
            if not self.execute_cycle():
                return
            yield self.output

    def execute_cycles(self, cycle_count: int) -> int:
        return sum(1 for _ in self.iter_cycles(cycle_count))


class Instruction(ABC):
    @staticmethod
    def from_str(instruction: str) -> 'Instruction':
        s = instruction.split(' ', maxsplit=1)
        if s[0] == 'noop':
            return Noop()
        elif s[0] == 'addx':
            return AddX(s[1])

    @abstractmethod
    def run_cycle(self, state: State) -> bool:
        # returns if instruction has completed or not
        raise NotImplemented


class Noop(Instruction):
    def __init__(self):
        pass

    def run_cycle(self, state: State) -> bool:
        return True


class AddX(Instruction):
    def __init__(self, value: str):
        self.value = int(value)
        self.cycle_count = 0

    def run_cycle(self, state: State) -> bool:
        self.cycle_count += 1
        if self.cycle_count == 2:
            state.register += self.value
            return True
        return self.cycle_count > 1


def read_input(input_str: str) -> Deque[Instruction]:
    return deque((Instruction.from_str(line) for line in line_iterator(input_str)))


def d10p1_solution(input_str: str) -> str:
    state = State(read_input(input_str))
    signal_strengths = 0
    for i in count(20, 40):
        # we need the value as it will be at start of next cycle
        state.execute_cycles(i - state.cycle_num)
        if state.cycle_num < i:
            break
        signal_strengths += state.cycle_num * state.output
    return str(signal_strengths)


def d10p2_solution(input_str: str) -> str:
    # choose your output pixel characters
    # p_on, p_off = '#', '.'    # match the example given by the challenge
    p_on, p_off = '█', ' '      # clearer, easier to see the result
    # p_on, p_off = '♥', '♡'    # spread some love
    # p_on, p_off = 'U', 'w'    # UwU

    state = State(read_input(input_str))
    grid: List[List[str]] = [[' '] * 40 for _ in range(6)]

    for i, sprite_pos in enumerate(state.iter_cycles(40 * 6 - 1)):
        x, y = i % 40, i // 40
        grid[y][x] = p_on if abs(sprite_pos - x) < 2 else p_off
    return '\n'.join((''.join(grid[y]) for y in range(6)))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=10, part=1)
    run_puzzle(day=10, part=2)
