from typing import Iterator

from common import line_iterator


class SectionGroup:
    def __init__(self, from_section: int, to_section: int):
        if from_section > to_section:
            raise RuntimeError()
        self.from_section = from_section
        self.to_section = to_section

    def is_contained_in(self, other: 'SectionGroup') -> bool:
        return self.from_section >= other.from_section and self.to_section <= other.to_section

    def overlaps_with(self, other: 'SectionGroup') -> bool:
        if self.from_section < other.from_section:
            return self.to_section >= other.from_section
        else:
            return self.from_section <= other.to_section

    @classmethod
    def from_str(cls, s: str) -> 'SectionGroup':
        ints = [int(i.strip()) for i in s.split('-', maxsplit=1)]
        return cls(from_section=ints[0], to_section=ints[1])


class ElfPair:
    def __init__(self, first_elf: SectionGroup, second_elf: SectionGroup):
        self.first_elf = first_elf
        self.second_elf = second_elf


def iter_elf_pairs(input_str: str) -> Iterator[ElfPair]:
    for line in line_iterator(input_str):
        elves = [SectionGroup.from_str(s) for s in line.split(',', maxsplit=1)]
        yield ElfPair(first_elf=elves[0], second_elf=elves[1])


def d4p1_solution(input_str: str) -> str:
    fully_contained_count = 0
    for elf_pair in iter_elf_pairs(input_str):
        if elf_pair.first_elf.is_contained_in(elf_pair.second_elf) \
                or elf_pair.second_elf.is_contained_in(elf_pair.first_elf):
            fully_contained_count += 1
    return str(fully_contained_count)


def d4p2_solution(input_str: str) -> str:
    return str(sum(pair.first_elf.overlaps_with(pair.second_elf) for pair in iter_elf_pairs(input_str)))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=4, part=1)
    run_puzzle(day=4, part=2)
