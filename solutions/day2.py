import re
from enum import Enum
from typing import List, Tuple, Iterator, Dict

from common import line_iterator


class Shape(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Outcome(Enum):
    Loss = 0
    Draw = 3
    Win = 6


# precompiled constants
results: Dict[Shape, Dict[Shape, Outcome]] = {
    Shape.Rock:     {Shape.Rock: Outcome.Draw, Shape.Paper: Outcome.Loss, Shape.Scissors: Outcome.Win},
    Shape.Paper:    {Shape.Rock: Outcome.Win, Shape.Paper: Outcome.Draw, Shape.Scissors: Outcome.Loss},
    Shape.Scissors: {Shape.Rock: Outcome.Loss, Shape.Paper: Outcome.Win, Shape.Scissors: Outcome.Draw}
}
desired_outcomes: Dict[Shape, Dict[Outcome, Shape]] = {sh: {} for sh in Shape}
for ys, rd in results.items():
    for os, out in rd.items():
        desired_outcomes[os][out] = ys

# input-related constants
line_regex = re.compile('^([ABC]) ([XYZ])$')
opponent_codes = {'A': Shape.Rock, 'B': Shape.Paper, 'C': Shape.Scissors}
your_codes = {'X': Shape.Rock, 'Y': Shape.Paper, 'Z': Shape.Scissors}
result_codes = {'X': Outcome.Loss, 'Y': Outcome.Draw, 'Z': Outcome.Win}


def play_round(your_shape: Shape, opponent_shape: Shape) -> int:
    res = results[your_shape][opponent_shape]
    return your_shape.value + res.value


def play_game(round_moves: List[Tuple[Shape, Shape]]) -> int:
    # round_moves: [(your_move, opponent_move), ...]
    return sum(play_round(your_sh, opp_sh) for your_sh, opp_sh in round_moves)


def iter_guide_lines(input_str: str) -> Iterator[Tuple[str, str]]:
    for line in line_iterator(input_str):
        match = line_regex.match(line)
        if match is None:
            raise RuntimeError('Invalid input')
        yield match[1], match[2]


def d2p1_solution(input_str: str) -> str:
    # read the guide (incorrectly)
    guide: List[Tuple[Shape, Shape]] = []
    for opp_code, your_code in iter_guide_lines(input_str):
        guide.append((opponent_codes[opp_code], your_codes[your_code]))

    # play game and return score
    moves = [(ym, om) for om, ym in guide]
    return str(play_game(moves))


def d2p2_solution(input_str: str) -> str:
    # read the guide (correctly)
    guide: List[Tuple[Shape, Outcome]] = []
    for opp_code, res_code in iter_guide_lines(input_str):
        guide.append((opponent_codes[opp_code], result_codes[res_code]))

    # calculate our moves from desired outcomes
    moves: List[Tuple[Shape, Shape]] = [(desired_outcomes[opp_sh][outcome], opp_sh) for opp_sh, outcome in guide]

    # play game and return score
    return str(play_game(moves))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=2, part=1)
    run_puzzle(day=2, part=2)
