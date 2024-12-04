# Ceres Search - https://adventofcode.com/2024/day/4
from collections import defaultdict
from itertools import product


def get_data(filename: str) -> dict[tuple[int, int], str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    res = defaultdict(lambda: "")
    for y, x in product(range(len(lines)), range(len(lines[0]))):
        res[(y, x)] = lines[y][x]
    return res


def q1(filename: str) -> int:
    data = get_data(filename)

    count = 0
    for y, x in list(data.keys()):
        for dy, dx in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            w = data[(y, x)] + data[(y + dy, x + dx)] + data[(y + 2 * dy, x + 2 * dx)] + data[(y + 3 * dy, x + 3 * dx)]
            if w == 'XMAS':
                count += 1
    return count


def q2(filename: str) -> int:
    data = get_data(filename)

    count = 0
    for y, x in list(data.keys()):
        if data[(y, x)] == 'A':
            w = data[(y - 1, x - 1)] + data[(y - 1, x + 1)] + data[(y + 1, x - 1)] + data[(y + 1, x + 1)]
            if ''.join(sorted(w)) == "MMSS" and data[(y - 1, x - 1)] != data[(y + 1, x + 1)]:
                count += 1
    return count


def test_q1():
    assert q1("test.txt") == 18
    assert q1("data.txt") == 2358


def test_q2():
    assert q2("test.txt") == 9
    assert q2("data.txt") == 1737
