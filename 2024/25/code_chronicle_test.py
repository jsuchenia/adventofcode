# Code Chronicle - https://adventofcode.com/2024/day/25
from itertools import product

from aoclib import parse_map


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().split("\n\n")


def q1(filename: str) -> int:
    data = get_data(filename)
    locks = []
    keys = []

    for pattern in data:
        encoded = set(parse_map(pattern.splitlines(), skip_chars='.').keys())
        if pattern.startswith("#####"):
            locks.append(encoded)
        else:
            keys.append(encoded)

    return sum(key.isdisjoint(lock) for key, lock in product(keys, locks))


def test_q1():
    assert q1("test.txt") == 3
    assert q1("data.txt") == 2950
