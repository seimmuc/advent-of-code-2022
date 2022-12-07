import re
from dataclasses import dataclass, field
from os.path import normpath
from pathlib import PurePath
from typing import Dict, Union, Iterator, Tuple

from common import line_iterator


cmd_regex = re.compile(r'\$ (cd|ls)(?: ([\S]+))?')
ls_out_regex = re.compile(r'(\d+|dir) (\S+)')


class ShellState:
    def __init__(self):
        self.cur_dir = PurePath('/')
        self.ls_output = False


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str
    contents: Dict[str, Union[File, 'Dir']] = field(default_factory=dict)

    @property
    def total_size(self) -> int:
        ts = 0
        for _, c in self.contents.items():
            if isinstance(c, Dir):
                ts += c.total_size
            else:
                ts += c.size
        return ts


def execute_cmd(state: ShellState, line: str):
    cmd_match = cmd_regex.match(line)
    if cmd_match[1] == 'cd':
        state.cur_dir = PurePath(normpath(state.cur_dir.joinpath(cmd_match[2].strip())))
    elif cmd_match[1] == 'ls':
        state.ls_output = True


def process_ls_line(state: ShellState, dir_tree: Dir, line: str):
    cd: Dir = dir_tree
    for i, d in enumerate(state.cur_dir.parts):
        d = d.strip()
        if not d or (i == 0 and d == '/'):
            continue
        cd = cd.contents[d]
        if not isinstance(cd, Dir):
            raise RuntimeError(f'Error parsing ls output: directory not yet scanned: {line}')
    match = ls_out_regex.match(line)
    if match[1] == 'dir':
        cd.contents[match[2]] = Dir(match[2])
    else:
        cd.contents[match[2]] = File(match[2], int(match[1]))


def parse_input(input_str: str) -> Dir:
    state = ShellState()
    dir_tree: Dir = Dir('/')
    for line in line_iterator(input_str):
        if line.startswith('$'):
            state.ls_output = False
            execute_cmd(state, line)
        else:
            if state.ls_output:
                process_ls_line(state, dir_tree, line)
            else:
                raise RuntimeError(f'Invalid input: unexpected output line: {line}')
    return dir_tree


def dir_iter(root_dir: Dir) -> Iterator[Union[Dir, File]]:
    yield root_dir
    for c in root_dir.contents.values():
        if isinstance(c, Dir):
            for dc in dir_iter(c):
                yield dc
        else:
            yield c


def d7p1_solution(input_str: str) -> str:
    res = 0
    dir_tree = parse_input(input_str)
    for item in dir_iter(dir_tree):
        if isinstance(item, Dir):
            ds = item.total_size
            if ds <= 100000:
                res += ds
    return str(res)


def d7p2_solution(input_str: str) -> str:
    total_space, space_needed = 70000000, 30000000
    dir_tree = parse_input(input_str)
    free_space = total_space - dir_tree.total_size
    to_delete: Tuple[int, Dir] = (total_space, dir_tree)
    for item in dir_iter(dir_tree):
        if isinstance(item, Dir):
            ds = item.total_size
            if free_space + ds >= space_needed and ds < to_delete[0]:
                to_delete = (ds, item)
    return str(to_delete[0])


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=7, part=1)
    run_puzzle(day=7, part=2)
