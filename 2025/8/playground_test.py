# Playground - https://adventofcode.com/2025/day/8
from itertools import combinations
from math import prod, dist

from networkx import Graph, connected_components, is_connected

from aoclib import *


def get_data(filename: str) -> set[tuple[int, ...]]:
    with open(filename) as f:
        return {ints(line) for line in f.read().strip().splitlines()}


def q1(filename: str, size: int) -> int:
    points = get_data(filename)
    distances = sorted([(dist(a, b), a, b) for a, b in combinations(points, 2)], key=lambda x: x[0])

    g = Graph()
    for _, a, b in distances[:size]:
        g.add_edge(a, b)

    sizes = sorted([len(c) for c in connected_components(g)], reverse=True)
    return prod(sizes[:3])


def q2(filename: str) -> int:
    points = get_data(filename)
    visited = set()  # for performance, it's easier to check sets than is_connected() each time
    distances = sorted([(dist(a, b), a, b) for a, b in combinations(points, 2)], key=lambda x: x[0])

    g = Graph()
    g.add_nodes_from(points)

    for _, a, b in distances:
        g.add_edge(a, b)
        visited.update({a, b})
        if points == visited and is_connected(g):
            return a[0] * b[0]
    return -1


def test_q1():
    assert q1("test.txt", 10) == 40
    assert q1("data.txt", 1000) == 80446


def test_q2():
    assert q2("test.txt") == 25272
    assert q2("data.txt") == 51294528
