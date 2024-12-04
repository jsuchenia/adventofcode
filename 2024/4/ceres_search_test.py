# Ceres Search - https://adventofcode.com/2024/day/4
from itertools import product


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return lines


def q1(filename: str) -> int:
    data = get_data(filename)

    def val(y, x) -> str:
        if 0 <= y < len(data) and 0 <= x < len(data[0]):
            return data[y][x]
        return ''

    count = 0
    for y, x in product(range(len(data)), range(len(data[0]))):
        for dy, dx in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            w = val(y, x) + val(y + dy, x + dx) + val(y + 2 * dy, x + 2 * dx) + val(y + 3 * dy, x + 3 * dx)
            if w == 'XMAS':
                count += 1
    return count


def q2(filename: str) -> int:
    data = get_data(filename)

    def val(y, x) -> str:
        if 0 <= y < len(data) and 0 <= x < len(data[0]):
            return data[y][x]
        return ''

    count = 0
    for y, x in product(range(len(data)), range(len(data[0]))):
        if val(y, x) == 'A':
            w = val(y - 1, x - 1) + val(y - 1, x + 1) + val(y + 1, x - 1) + val(y + 1, x + 1)
            if ''.join(sorted(w)) == "MMSS" and val(y - 1, x - 1) != val(y + 1, x + 1):
                count += 1
    return count


def test_q1():
    assert q1("test.txt") == 18
    assert q1("data.txt") == 2358


def test_q2():
    assert q2("test.txt") == 9
    assert q2("data.txt") == 1737
