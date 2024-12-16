# Garden Groups - https://adventofcode.com/2024/day/12
# Use NetworkX to separate graphs and Shapely to calculate area and boundaries


from networkx.algorithms.components import is_connected, connected_components
from networkx.classes import Graph
from shapely import box, union_all

from aoclib import *


def get_data(filename: str) -> dict[complex, str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    area = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            area[y + 1j * x] = c
    return area


def get_separated_polygons(filename: str):
    data = get_data(filename)

    g = Graph()
    for point in data.keys():
        g.add_node(point)
        for direction in DIRECTIONS_4:
            if data[point] == data.get(point + direction, ""):
                g.add_edge(point, point + direction)
    assert is_connected(g) is False

    for nodes in connected_components(g):
        boxes = [box(point.imag, point.real, point.imag + 1, point.real + 1) for point in nodes]
        yield union_all(boxes)


def q1(filename: str) -> int:
    return sum(polygon.area * polygon.boundary.length for polygon in get_separated_polygons(filename))


def q2(filename: str) -> int:
    result = 0
    for polygon in get_separated_polygons(filename):
        boundary = polygon.boundary.normalize().simplify(0.0)
        if boundary.is_ring:
            result += polygon.area * (len(boundary.coords) - 1)
        else:  # some interior elements are there
            for line in boundary.geoms:
                result += polygon.area * (len(line.coords) - 1)
    return result


def test_q1():
    assert q1("test1.txt") == 140
    assert q1("test2.txt") == 772
    assert q1("test3.txt") == 1930
    assert q1("data.txt") == 1361494


def test_q2():
    assert q2("test1.txt") == 80
    assert q2("test2.txt") == 436
    assert q2("test3.txt") == 1206
    assert q2("data.txt") == 830516
