# Trash Compactor - https://adventofcode.com/2025/day/6

from math import prod
from typing import Sequence

OP = {'+': sum, '*': prod}
getchar = lambda line, i: line[i] if i < len(line) else " "


def get_data_q1(filename: str) -> list[tuple[str]]:
    with open(filename) as f:
        lines = [line.split() for line in f.read().strip().splitlines()]
    return list(zip(*lines[::-1]))


def get_data_q2(filename: str) -> list[list[str]]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    result = []
    for i in range(max([len(line) for line in lines])):
        if ch := getchar(lines[-1], i).strip():
            result.append([ch])
        if num := ''.join([getchar(line, i) for line in lines[:-1]]).strip():
            result[-1].append(num)
    return result


def calc(lines: list[Sequence[str]]) -> int:
    return sum([OP[op](list(map(int, nums))) for op, *nums in lines])


def q1(filename: str) -> int:
    return calc(get_data_q1(filename))


def q2(filename: str) -> int:
    return calc(get_data_q2(filename))


def test_q1():
    assert q1("test.txt") == 4277556
    assert q1("data.txt") == 5316572080628


def test_q2():
    assert q2("test.txt") == 3263827
    assert q2("data.txt") == 11299263623062
