# Red-Nosed Reports - https://adventofcode.com/2024/day/2
from itertools import pairwise

from aoclib import *


def get_data(filename: str) -> list[tuple[int, ...]]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    return [ints(line) for line in lines]


def is_safe(level: tuple[int, ...]) -> bool:
    diffs = [b - a for a, b in pairwise(level)]

    return all(-1 >= diff >= -3 for diff in diffs) or all(1 <= diff <= 3 for diff in diffs)


def q1(filename: str) -> int:
    levels = get_data(filename)

    return sum(1 for level in levels if is_safe(level))


def q2(filename: str) -> int:
    levels = get_data(filename)
    safe_count = 0

    for level in levels:
        level_reduced = (level[:i] + level[i + 1:] for i in range(len(level)))
        if any(is_safe(pattern) for pattern in level_reduced):
            safe_count += 1

    return safe_count


def test_q1():
    assert q1("test.txt") == 2
    assert q1("data.txt") == 598


def test_q2():
    assert q2("test.txt") == 4
    assert q2("data.txt") == 634
