from collections import deque


def find_unique_char_end(datastream: str, char_count: int) -> int:
    char_buf = deque(maxlen=char_count)
    for i, c in enumerate(datastream):
        char_buf.append(c)
        if len(char_buf) < char_count:
            continue
        if len(set(char_buf)) == char_count:
            return i + 1


def d6p1_solution(input_str: str) -> str:
    return str(find_unique_char_end(input_str, char_count=4))


def d6p2_solution(input_str: str) -> str:
    return str(find_unique_char_end(input_str, char_count=14))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=6, part=1)
    run_puzzle(day=6, part=2)
