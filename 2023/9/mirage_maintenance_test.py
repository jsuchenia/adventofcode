# Mirage Maintenance - https://adventofcode.com/2023/day/9
from itertools import pairwise


def get_data(filename: str) -> list[list[int]]:
    with open(filename) as f:
        lines = f.read().splitlines()
    lines = [[int(n) for n in line.split()] for line in lines]
    return lines


def guess_last(numbers: list[int]):
    if all([n == 0 for n in numbers]):
        return 0
    diff = [b - a for a, b in pairwise(numbers)]
    return numbers[-1] + guess_last(diff)


def guess_first(numbers: list[int]):
    if all([n == 0 for n in numbers]):
        return 0
    diff = [b - a for a, b in pairwise(numbers)]
    return numbers[0] - guess_first(diff)


def q1(filename: str) -> int:
    data = get_data(filename)
    return sum([guess_last(line) for line in data])


def q2(filename: str) -> int:
    data = get_data(filename)
    return sum([guess_first(line) for line in data])


def test_q1():
    assert q1("test.txt") == 114
    assert q1("data.txt") == 2005352194


def test_q2():
    assert q2("test.txt") == 2
    assert q2("data.txt") == 1077
