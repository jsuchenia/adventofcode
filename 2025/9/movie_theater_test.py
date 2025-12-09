# Movie Theater - https://adventofcode.com/2025/day/9
from itertools import combinations
from math import prod

from shapely import Polygon
from shapely.prepared import prep

from aoclib import *


def get_data(filename: str) -> list[tuple[int, ...]]:
    with open(filename) as f:
        return [ints(line) for line in f.read().strip().splitlines()]


def area(p1: tuple[int, ...], p2: tuple[int, ...]) -> int:
    return prod(abs(a - b) + 1 for a, b in zip(p1, p2))


def rectangle(p1: tuple[int, ...], p2: tuple[int, ...]) -> Polygon:
    return Polygon([(p1[0], p1[1]), (p2[0], p1[1]), (p2[0], p2[1]), (p1[0], p2[1])])


def q1(filename: str) -> int:
    data = get_data(filename)
    return max(area(p1, p2) for p1, p2 in combinations(data, 2))


def q2(filename: str) -> int:
    data = get_data(filename)
    polygon = Polygon(data)
    prepared_polygon = prep(polygon)
    return max(area(p1, p2) for p1, p2 in combinations(data, 2) if prepared_polygon.covers(rectangle(p1, p2)))


def test_q1():
    assert q1("test.txt") == 50
    assert q1("data.txt") == 4748985168


def test_q2():
    assert q2("test.txt") == 24
    assert q2("data.txt") == 1550760868
