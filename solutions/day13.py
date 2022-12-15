import json
from functools import cmp_to_key
from itertools import zip_longest
from typing import TypeVar, Iterator, Tuple, Union, List

from common import line_iterator


PacketType = Union[int, List]


def compare(left_packet: PacketType, right_packet: PacketType) -> int:
    if isinstance(left_packet, int) and isinstance(right_packet, int):
        return left_packet - right_packet
    if isinstance(left_packet, list) and isinstance(right_packet, list):
        for left, right in zip_longest(left_packet, right_packet, fillvalue=None):
            if left is None and right is None:
                return 0
            if left is None:
                return -1
            if right is None:
                return 1
            res = compare(left_packet=left, right_packet=right)
            if res != 0:
                return res
        return 0
    if isinstance(left_packet, int):
        return compare(left_packet=[left_packet], right_packet=right_packet)
    else:
        return compare(left_packet=left_packet, right_packet=[right_packet])


def read_input(input_str: str) -> List[Tuple[PacketType, PacketType]]:
    packet_pairs: List[Tuple[PacketType, PacketType]] = []
    for lstr, rstr, _ in zip_longest(*([line_iterator(input_str)] * 3)):
        packet_pairs.append((json.loads(lstr), json.loads(rstr)))
    return packet_pairs


def d13p1_solution(input_str: str) -> str:
    packet_pairs = read_input(input_str)
    index_sum = 0
    for i, (lp, rp) in enumerate(packet_pairs):
        if compare(left_packet=lp, right_packet=rp) <= 0:
            index_sum += i + 1
    return str(index_sum)


def d13p2_solution(input_str: str) -> str:
    dp1, dp2 = [[2]], [[6]]
    packet_pairs = read_input(input_str)
    all_packets = [p for pair in packet_pairs for p in pair]
    all_packets.extend((dp1, dp2))
    all_packets.sort(key=cmp_to_key(compare))
    res = (all_packets.index(dp1) + 1) * (all_packets.index(dp2) + 1)
    return str(res)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=13, part=1)
    run_puzzle(day=13, part=2)
