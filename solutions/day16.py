import re
from collections import deque
from itertools import chain
from typing import List, Tuple, Dict, Deque, Set, Optional, Iterable

from common import line_iterator


valve_regex = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)')


class Valve:
    def __init__(self, name: str, flow_rate: int):
        self.name = name
        self.flow_rate = flow_rate

        self.tunnels: List[Valve] = []
        self.shortest_paths: Dict[str, List[str]] = {}

    def set_tunnels(self, all_valves: Dict[str, 'Valve'], valve_names: List[str]):
        self.tunnels = [all_valves[vn] for vn in valve_names]

    def calculate_paths(self, all_valves: Dict[str, 'Valve'], destinations: Set[str]):
        self.shortest_paths = find_paths(valves=all_valves, from_valve=self, destinations=destinations)


class State:
    def __init__(self, valves: Dict[str, Valve], current_location: str):
        self.valves = valves
        self.current_location = current_location
        self.pressure_released = 0
        self.minutes_left = 30
        self.valves_open: Set[str] = set()
        self.current_move: Optional[Tuple[List[str], int]] = None
        self.opening_valve: bool = False
        self.arrived = False

    def copy(self) -> 'State':
        new = State(valves=self.valves, current_location=self.current_location)
        new.pressure_released = self.pressure_released
        new.minutes_left = self.minutes_left
        new.valves_open = self.valves_open.copy()
        new.current_move = self.current_move
        new.opening_valve = self.opening_valve
        new.arrived = self.arrived
        return new

    @property
    def current_valve(self) -> Valve:
        return self.valves[self.current_location]

    @property
    def is_moving(self) -> bool:
        return self.current_move is not None

    def start_move(self, move: List[str]):
        self.current_move = (move, 0)

    def start_open(self):
        self.opening_valve = True

    def minute_passed(self, valves: Dict[str, Valve]) -> bool:
        if self.minutes_left < 1:
            return False

        # tick minute
        self.minutes_left -= 1

        # move if applicable
        self.arrived = False
        if self.current_move is not None:
            move, i = self.current_move
            self.current_location = move[i]
            if i + 1 < len(move):
                self.current_move = (move, i + 1)
            else:
                self.current_move = None
                self.arrived = True

        # calculate pressure release
        for valve in valves.values():
            if valve.name in self.valves_open:
                self.pressure_released += valve.flow_rate

        # open current valve
        if self.opening_valve:
            self.valves_open.add(self.current_location)
            self.opening_valve = False

        return True

    def act_or_think(self) -> Optional[List[Tuple[float, List[str]]]]:
        # continue with current move
        if self.is_moving:
            return None
        # if we just arrived to our destination, spend minute opening valve
        if self.arrived and self.current_location not in self.valves_open:
            self.start_open()
            return None
        # get remaining closed valves we can reach
        reachable_valves_remaining = [(d, p) for d, p in self.current_valve.shortest_paths.items()
                                      if d not in self.valves_open]
        if not reachable_valves_remaining:
            return None
        # rank our options for next valve to open and return the result
        scores: List[Tuple[float, List[str]]] = []
        for destination_name, path in reachable_valves_remaining:
            dv = self.valves[destination_name]
            dist = len(path)
            scores.append((dv.flow_rate / dist, path))
        scores.sort(key=lambda e: e[0], reverse=True)
        return scores


def find_paths(valves: Dict[str, Valve], from_valve: Valve, destinations: Set[str]) -> Dict[str, List[str]]:
    solutions: Dict[str, List[str]] = {}
    reached: Set[str] = {from_valve.name}
    last_steps: Deque[Deque[str]] = deque((deque(),))
    while last_steps and destinations:
        new_steps: Deque[Deque[str]] = deque()
        while last_steps and destinations:
            path = last_steps.popleft()
            current_valve = valves[path[-1]] if path else from_valve
            for new_valve in current_valve.tunnels:
                if new_valve.name in reached:
                    continue
                new_path = path.copy()
                new_path.append(new_valve.name)
                new_steps.append(new_path)
                reached.add(new_valve.name)
                if new_valve.name in destinations:
                    destinations.remove(new_valve.name)
                    solutions[new_valve.name] = list(new_path)
        last_steps = new_steps
    return solutions


def read_input(input_str: str) -> Dict[str, Valve]:
    valves: Dict[str, Valve] = {}
    vl: List[Tuple[Valve, List[str]]] = []

    for line in line_iterator(input_str):
        match = valve_regex.match(line)
        v = Valve(name=match[1], flow_rate=int(match[2]))
        vl.append((v, list(map(str.strip, match[3].split(',')))))
        valves[v.name] = v

    for v, tun_list in vl:
        v.set_tunnels(all_valves=valves, valve_names=tun_list)

    return valves


def d16p1_solution(input_str: str) -> str:
    alternatives = 2

    valves = read_input(input_str)
    functional_valves = [v for v in valves.values() if v.flow_rate > 0]
    for valve in chain((valves['AA'],), functional_valves):
        valve.calculate_paths(all_valves=valves, destinations={d.name for d in functional_valves if d != valve})

    states: Deque[State] = deque([State(valves=valves, current_location='AA')])
    results: List[State] = []
    while states:
        state = states.popleft()
        while state.minutes_left > 0:
            options = state.act_or_think()
            if options is not None:
                copies: Iterable[State] = chain((state,), (state.copy() for _ in range(alternatives)))
                for c, o in zip(copies, options):
                    c.start_move(o[1])
                    if c != state:
                        states.append(c)
            state.minute_passed(valves=valves)
        results.append(state)
    results.sort(key=lambda s: s.pressure_released, reverse=True)
    # print(len(results))

    return str(results[0].pressure_released)


def d16p2_solution(input_str: str) -> str:
    # valves = read_input(input_str)
    return None


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=16, part=1)
    run_puzzle(day=16, part=2)
