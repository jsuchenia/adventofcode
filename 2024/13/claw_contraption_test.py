# Claw Contraption - https://adventofcode.com/2024/day/13
import re

from sympy import symbols, Eq, solve


def get_data(filename: str) -> list[list[int]]:
    with open(filename) as f:
        return [
            [int(n) for n in re.findall(r'(\d+)', machine)]
            for machine in f.read().strip().split('\n\n')
        ]


def q1(filename: str, *, boost=0) -> int:
    tokens = 0
    machines = get_data(filename)
    for machine in machines:
        a, b = symbols("a b", integer=True, nonnegative=True)

        result = solve([
            Eq(a * machine[0] + b * machine[2], machine[4] + boost),
            Eq(a * machine[1] + b * machine[3], machine[5] + boost),
        ], [a, b])

        if result:
            tokens += 3 * result[a] + result[b]

    return tokens


def test_q1():
    assert q1("test.txt") == 480
    assert q1("data.txt") == 29711


def test_q2():
    assert q1("test.txt", boost=10_000_000_000_000) == 875318608908
    assert q1("data.txt", boost=10_000_000_000_000) == 94955433618919
