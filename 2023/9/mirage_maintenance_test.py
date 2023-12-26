# Mirage Maintenance - https://adventofcode.com/2023/day/9
from itertools import pairwise

import pytest

def get_data(filename: str) -> list[list[int]]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
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

@pytest.mark.parametrize("filename, result", [("test.txt", 114), ("data.txt", 2005352194)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 2), ("data.txt", 1077)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
