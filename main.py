from importlib import import_module
from pathlib import Path

from common import load_input_from_file, PuzzleSolution


def run_puzzle(day: int, part: int):
    puzzle_id = f'd{day}p{part}'
    mod_name = f'day{day}'

    solution_name = f'{puzzle_id}_solution'
    solution_module = import_module(f'solutions.{mod_name}')
    solution_function: PuzzleSolution = getattr(solution_module, solution_name)

    puzzle_input_file = Path('inputs', f'd{day}p{part}_input.txt')
    if not puzzle_input_file.is_file():
        puzzle_input_file = Path(puzzle_input_file.parent, f'd{day}_input.txt')
        if not puzzle_input_file.is_file():
            raise RuntimeError(f'{puzzle_id} is missing an input file')
    puzzle_input = load_input_from_file(puzzle_input_file)

    print(f'Solving {puzzle_id} puzzle')
    solution_output = solution_function(puzzle_input)
    if isinstance(solution_output, str):
        print('Done, printing solution')
        print('=======================')
        print(solution_output)
        print('=======================')
    else:
        print(f'Error: solution output is of invalid type: {type(solution_output)}')


if __name__ == '__main__':
    run_puzzle(day=1, part=2)
