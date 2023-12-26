# Lens Library - https://adventofcode.com/2023/day/15
from collections import defaultdict
from functools import reduce

import pytest

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().split(',')

def HASH(s: str) -> int:
    return reduce(lambda h, c: ((h + ord(c)) * 17) % 256, s, 0)

def q1(filename: str) -> int:
    return sum(HASH(s) for s in get_data(filename))

def q2(filename: str) -> int:
    # Since python 3.7 built-in dict keeps an order of an insertion
    # https://docs.python.org/3/library/collections.html#ordereddict-objects

    boxes = defaultdict(dict)
    for s in get_data(filename):
        match s.strip('-').split('='):
            case [label, value]:
                boxes[HASH(label)][label] = int(value)
            case [label]:
                boxes[HASH(label)].pop(label, None)

    return sum(
        (box + 1) * idx * value
        for box, lenses in boxes.items()
        for idx, value in enumerate(lenses.values(), start=1))

def test_hash():
    assert HASH("HASH") == 52

@pytest.mark.parametrize("filename, result", [("test.txt", 1320), ("data.txt", 507291)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 145), ("data.txt", 296921)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
