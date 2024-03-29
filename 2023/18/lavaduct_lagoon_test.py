# Lavaduct Lagoon - https://adventofcode.com/2023/day/18
import re

import matplotlib.pyplot as plt
import pytest
# This is what we learned during day 10
from shapely import Point, Polygon

def get_data(filename: str) -> list[tuple]:
    with open(filename) as f:
        return [re.match(r"(\w) (\d+) \(#(.*)\)", line).groups() for line in f.read().strip().splitlines()]

def q1(filename: str, img_name=None) -> int:
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
    if img_name:
        x, y = p.exterior.xy
        plt.xscale('linear')
        plt.yscale('linear')
        plt.title(img_name)
        plt.plot(x, y)
        plt.savefig(img_name)

    return int(p.area + p.length / 2 + 1)

def q2(filename: str, img_name=None) -> int:
    data = get_data(filename)
    x = y = 0
    points = [Point(x, y)]
    for _, _, rgb in data:
        value = int(rgb[:-1], 16)
        direction = rgb[-1:]
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
    if img_name:
        x, y = p.exterior.xy
        plt.xscale('linear')
        plt.yscale('linear')
        plt.title(img_name)
        plt.plot(x, y)
        plt.savefig(img_name)
    return int(p.area + p.length / 2 + 1)

@pytest.mark.parametrize("filename, result", [("test.txt", 62), ("data.txt", 52035)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 952408144115), ("data.txt", 60612092439765)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
