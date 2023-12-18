# Lavaduct Lagoon - https://adventofcode.com/2023/day/18
import re

# This is what we learned during day 10
from shapely import Point, Polygon

def get_data(filename: str) -> list[tuple]:
    with open(filename) as f:
        return [re.match(r"(\w) (\d+) \(#(.*)\)", line).groups() for line in f.read().splitlines()]

def q1(filename: str) -> int:
    data = get_data(filename)
    x = y = 0
    points = [Point(x, y)]
    for direction, step, _ in data:
        val = int(step)
        if direction == "R":
            x += val
        elif direction == "L":
            x -= val
        elif direction == "U":
            y -= val
        elif direction == "D":
            y += val
        points.append(Point(x, y))

    p = Polygon(points)
    return int(p.area + p.length / 2 + 1)

def q2(filename: str) -> int:
    data = get_data(filename)
    x = y = 0
    points = [Point(x, y)]
    for _, _, h in data:
        value = int(h[:-1], 16)
        direction = h[-1:]
        if direction == "0":
            x += value
        elif direction == "2":
            x -= value
        elif direction == "3":
            y -= value
        elif direction == "1":
            y += value
        points.append(Point(x, y))

    p = Polygon(points)
    return int(p.area + p.length / 2 + 1)

def test_q1():
    assert q1("test.txt") == 62
    assert q1("data.txt") == 52035

def test_q2():
    assert q2("test.txt") == 952408144115
    assert q2("data.txt") == 60612092439765
