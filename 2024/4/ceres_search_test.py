# Ceres Search - https://adventofcode.com/2024/day/4
from collections import defaultdict
from itertools import product

from aoclib import *


def get_data(filename: str) -> dict[AoCPoint, str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    res = defaultdict(lambda: "")
    for y, x in product(range(len(lines)), range(len(lines[0]))):
        res[AoCPoint(x=x, y=y)] = lines[y][x]
    return res


def q1(filename: str) -> int:
    data = get_data(filename)

    count = 0
    for point in list(data.keys()):
        for d in DIRECTIONS_8:
            w = data[point] + data[point + d] + data[point + 2 * d] + data[point + 3 * d]
            if w == 'XMAS':
                count += 1
    return count


def q2(filename: str) -> int:
    data = get_data(filename)

    count = 0
    for point in list(data.keys()):
        if data[point] == 'A':
            w = data[point + NE] + data[point + NW] + data[point + SE] + data[point + SW]
            if ''.join(sorted(w)) == "MMSS" and data[point + SE] != data[point + NW]:
                count += 1
    return count


def test_q1():
    assert q1("test.txt") == 18
    assert q1("data.txt") == 2358


def test_q2():
    assert q2("test.txt") == 9
    assert q2("data.txt") == 1737
