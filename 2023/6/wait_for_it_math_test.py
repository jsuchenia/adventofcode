# Improvements wrote after an initial implementation
# First I used sympy but as it caused issue with test data for q1, I created manual math

import re
from math import sqrt, prod


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


def calc_results(t, distance) -> int:
    # Solver has wrong calculations (too big by 1) for small numbers - trying to check why...

    # x * (t - x) - distance > 0
    # -x^2 + t*x - distance > 0
    # a = -1, b = +t, c= -distance
    # delta = t^2 -4 * (-1) * -(-distance)
    # delta = t^2 -4 * distance
    # x1 = -t -sqrt(delta) / (2 * -1)
    # x2 = -t +sqrt(delta) / (2 * -1)

    delta = t**2 - (4 * distance)
    x1 = (t + sqrt(delta)) / 2
    x2 = (-t + sqrt(delta)) / -2

    if x1 % 1 == 0:  # higher X is a number without fractional part, so distance is equal, but we have to win
        return int(x1) - int(x2) - 1
    return int(x1) - int(x2)


def q1_calc(filename) -> int:
    times, distances = get_data_q1(filename)

    return prod([calc_results(t, distance) for t, distance in zip(times, distances)])


def q2_brute(filename) -> int:
    t, distance = get_data_q2(filename)

    return [x * (t - x) > distance for x in range(t)].count(True)


def q2_calc(filename) -> int:
    t, distance = get_data_q2(filename)

    return calc_results(t, distance)


def test_q1_calc():
    assert q1_calc("test.txt") == 288
    assert q1_calc("data.txt") == 503424


def test_q2_calc():
    assert q2_calc("test.txt") == 71503
    assert q2_calc("data.txt") == 32607562
