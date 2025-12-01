# Secret Entrance - https://adventofcode.com/2025/day/1
from typing import Iterable


def get_data(filename: str) -> Iterable[int]:
    with open(filename) as f:
        for line in f.read().strip().splitlines():
            yield int(line[1:]) if line[0] == 'R' else -int(line[1:])


def q1(filename: str) -> int:
    current = 50
    count = 0

    for change in get_data(filename):
        current = (current + change) % 100
        count += current == 0
    return count


def q2(filename: str) -> int:
    current = 50
    count = 0

    for change in get_data(filename):
        current = (current + change) % 100

        count += current == 0
        count += abs(change) // 100

        # Extra cases - from positive to negative, and vice-versa
        count += change > 0 and current < (change % 100) and current != 0
        count += change < 0 and current > 100 - (abs(change) % 100)
    return count


def test_q1():
    assert q1("test.txt") == 3
    assert q1("data.txt") == 982


def test_q2():
    assert q2("test.txt") == 6
    assert q2("data.txt") == 6106
