# Historian Hysteria - https://adventofcode.com/2024/day/1
from collections import Counter

from aoclib import *


def get_data(filename: str) -> tuple[list[int], list[int]]:
    with open(filename) as f:
        lines = [ints(line) for line in f.read().strip().splitlines()]

    col1 = sorted(nums[0] for nums in lines)
    col2 = sorted(nums[1] for nums in lines)

    return col1, col2


def q1(filename: str) -> int:
    col1, col2 = get_data(filename)

    return sum(abs(b - a) for a, b in zip(col1, col2))


def q2(filename: str) -> int:
    col1, col2 = get_data(filename)

    count = Counter(col2)
    return sum(a * count[a] for a in col1)


def test_q1():
    assert q1("test.txt") == 11
    assert q1("data.txt") == 1603498


def test_q2():
    assert q2("test.txt") == 31
    assert q2("data.txt") == 25574739
