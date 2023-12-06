# Improvements wrote after an initial implementation

import re
from math import prod

from sympy import symbols, solve, Eq

def get_data_q1(filename: str):
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    times = [int(n) for n in re.findall(r"(\d+)", lines[0])]
    distances = [int(n) for n in re.findall(r"(\d+)", lines[1])]

    return times, distances


def get_data_q2(filename: str):
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    t = int(re.search(r"(\d+)", lines[0].replace(" ", ""))[1])
    distance = int(re.search(r"(\d+)", lines[1].replace(" ", ""))[1])

    return t, distance


def solve_results(t, distance) -> int:
    # x * (t - x) - distance = 0

    x = symbols("x")
    results = solve(Eq(x * (t - x) - distance, 0), [x])

    if results[1] % 1 == 0:  # higher X is a number without fractional part, so distance is equal, but we have to win
        return int(results[1]) - int(results[0]) - 1
    return int(results[1]) - int(results[0])


def q1(filename) -> int:
    times, distances = get_data_q1(filename)

    return prod([solve_results(t, distance) for t, distance in zip(times, distances)])


def q2(filename) -> int:
    t, distance = get_data_q2(filename)

    return solve_results(t, distance)


def test_q1_solve():
    assert q1("test.txt") == 288
    assert q1("data.txt") == 503424


def test_q2_solve():
    assert q2("test.txt") == 71503
    assert q2("data.txt") == 32607562
