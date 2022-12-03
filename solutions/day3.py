from typing import Tuple, Iterable, Set

from common import line_iterator


def get_priority(char: str) -> int:
    char_id = ord(char)
    if 97 <= char_id <= 122:
        return char_id - 96
    if 65 <= char_id <= 90:
        return char_id - 64 + 26
    raise RuntimeError('Invalid item character')


def intersection(iterables: Tuple[Iterable, ...]) -> Set:
    return set.intersection(*(set(it) for it in iterables))


def d3p1_solution(input_str: str) -> str:
    priority_sum = 0
    for line in line_iterator(input_str):
        if len(line) % 2 != 0:
            raise RuntimeError('rucksack contains odd number of items')
        lm = len(line) // 2
        shared_item = intersection((line[:lm], line[lm:]))
        if len(shared_item) != 1:
            raise RuntimeError(f'Invalid input: line "{line}" shares {len(shared_item)} items between compartments')
        priority_sum += get_priority(shared_item.pop())
    return str(priority_sum)


def d3p2_solution(input_str: str) -> str:
    priority_sum = 0
    for group in zip(*[line_iterator(input_str)] * 3):  # type: Tuple[str, str, str]
        # iterate over 3 lines at once
        shared_item = intersection(group)
        if len(shared_item) != 1:
            raise RuntimeError(f"Invalid input: group ({group}) has following shared items: {shared_item}")
        priority_sum += get_priority(shared_item.pop())
    return str(priority_sum)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=3, part=1)
    run_puzzle(day=3, part=2)
