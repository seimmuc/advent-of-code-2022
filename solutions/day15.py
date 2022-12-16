import re
import time
from collections import deque
from typing import List, Optional, Set, Deque, Iterator

from common import line_iterator, Pos


line_regex = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')


class Range:
    __slots__ = ['low', 'high']

    def __init__(self, low: int, high: int):
        if low > high:
            raise RuntimeError()
        self.low = low
        self.high = high

    def overlaps(self, other: 'Range') -> bool:
        if self.low < other.low:
            return self.high >= other.low
        else:
            return self.low <= other.high

    def combine(self, other: 'Range') -> Optional['Range']:
        if not self.overlaps(other):
            return None
        return Range(min(self.low, other.low), max(self.high, other.high))

    def intersect_with(self, other: 'Range') -> 'Range':
        return Range(max(self.low, other.low), min(self.high, other.high))

    def __iter__(self, step=1) -> Iterator[int]:
        return iter(range(self.low, self.high + 1, step))

    def __contains__(self, num: int):
        return self.low <= num <= self.high

    def __len__(self):
        return self.high - self.low + 1


class Sensor:
    __slots__ = ['pos_x', 'pos_y', 'beacon_pos', 'scan_distance']

    def __init__(self, sensor_pos: Pos, beacon_pos: Pos):
        self.pos_x = sensor_pos.x
        self.pos_y = sensor_pos.y
        self.beacon_pos = beacon_pos
        self.scan_distance = calc_dist(sensor_pos, beacon_pos)

    def row_scanned(self, row: int) -> Optional[Range]:
        dist_left = self.scan_distance - abs(self.pos_y - row)
        if dist_left >= 0:
            return Range(self.pos_x - dist_left, self.pos_x + dist_left)


def calc_dist(p1: Pos, p2: Pos) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def scan_row(sensors: List[Sensor], row: int, scan_range: Optional[Range] = None) -> Deque[Range]:
    # finds all scan ranges in a row, combining them if they overlap
    ranges: Deque[Range] = deque()
    for s in sensors:
        sr = s.row_scanned(row)
        if sr is None:
            continue
        while ranges:
            last_range = ranges.pop()
            if sr.overlaps(last_range):
                sr = sr.combine(last_range)
            else:
                ranges.append(last_range)
                break
        ranges.append(sr)
    if scan_range is None:
        return ranges
    return deque(r.intersect_with(scan_range) for r in ranges)


def read_input(input_str: str) -> List[Sensor]:
    sensor_list: List[Sensor] = []
    for line in line_iterator(input_str):
        match = line_regex.match(line)
        s = Sensor(sensor_pos=Pos(int(match[1]), int(match[2])), beacon_pos=Pos(int(match[3]), int(match[4])))
        sensor_list.append(s)
    return sensor_list


def d15p1_solution(input_str: str) -> str:
    y = 2000000

    sensors = read_input(input_str)
    sensors.sort(key=lambda s: s.pos_x)
    beacons: Set[Pos] = {s.beacon_pos for s in sensors}

    # scan row with all sensors, add up their scan ranges in that row
    ranges = scan_row(sensors=sensors, row=y)
    scanned_empty = sum(len(r) for r in ranges)

    # remove known beacons from the value
    for b in beacons:
        if b.y == y and any((b.x in r) for r in ranges):
            scanned_empty -= 1

    return str(scanned_empty)


def d15p2_solution(input_str: str) -> str:
    x_range = Range(low=0, high=4_000_000)
    y_range = Range(low=0, high=4_000_000)
    # x_range = Range(low=0, high=20)
    # y_range = Range(low=0, high=20)

    sensors = read_input(input_str)
    sensors.sort(key=lambda s: s.pos_x)

    first_empty_pos = None
    s_time = time.time()
    for y in y_range:
        ranges = scan_row(sensors, y, x_range)
        if sum(len(r) for r in ranges) < len(x_range):
            # found y, now need to find x
            x = x_range.low
            for r in ranges:
                if x not in r:
                    break
                x = r.high + 1
            if x not in x_range:
                raise RuntimeError()
            first_empty_pos = Pos(x=x, y=y)
            break
    print(f'scan completed in {time.time() - s_time:0.3f} seconds')

    if first_empty_pos is None:
        raise RuntimeError('No unscanned areas found in given ranges')

    return str(first_empty_pos.x * 4_000_000 + first_empty_pos.y)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=15, part=1)
    run_puzzle(day=15, part=2)
