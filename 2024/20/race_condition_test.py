# Race Condition - https://adventofcode.com/2024/day/20
from collections import defaultdict

from networkx import Graph, single_source_shortest_path_length, shortest_path
from scipy.spatial import KDTree

from aoclib import *


def get_data(filename: str) -> dict[complex, str]:
    with open(filename) as f:
        return parse_map(f.read().strip().splitlines())


def q1(filename: str, limit) -> int:
    area = get_data(filename)

    # get_map_as_img(area).save(f"map-{filename}.png")
    g_valid = Graph()
    start = None

    for point, val in area.items():
        if val == 'S':
            start = point
        if val != "#":
            g_valid.add_node(point)
            for neighbour in neighbors_4(point):
                if neighbour in g_valid:
                    g_valid.add_edge(point, neighbour)

    assert start is not None
    lengths = single_source_shortest_path_length(g_valid, start)
    shortcuts = defaultdict(list)

    for point, val in area.items():
        if val == '#':
            neighbor_values = [lengths[neighbour] for neighbour in neighbors_4(point) if neighbour in lengths]
            if len(neighbor_values) >= 2:
                shortcut = max(neighbor_values) - min(neighbor_values)
                shortcuts[shortcut - 2].append(point)

    # pprint(shortcuts)
    return sum(len(points) for saving, points in shortcuts.items() if saving >= limit)


def q2(filename: str, limit) -> int:
    area = get_data(filename)

    # Build a graph with only valid points
    g_valid = Graph()
    start = None
    end = None

    for point, val in area.items():
        if val == 'S':
            start = point
        if val == 'E':
            end = point
        if val != "#":
            g_valid.add_node(point)
            for neighbour in neighbors_4(point):
                if neighbour in g_valid:
                    g_valid.add_edge(point, neighbour)

    # Shortcuts needs to be on a shortest path, so index of a path is a distance from start
    lengths = {(point.real, point.imag): idx for idx, point in enumerate(shortest_path(g_valid, start, end))}
    positions = list(lengths.keys())

    # Look for points in a radius using Manhattan distance
    # Simple combinations(lengths.keys(), 2) took 6sec..

    shortcuts = 0
    kdtree = KDTree(positions)
    for point in lengths:
        # Radius r=20, p=1 is Manhattan distance
        for idx in kdtree.query_ball_point(point, r=20, p=1):
            neighbour = positions[idx]
            distance = abs(point[0] - neighbour[0]) + abs(point[1] - neighbour[1])

            if (abs(lengths[point] - lengths[neighbour]) - distance) >= limit:
                shortcuts += 1

    return shortcuts // 2  # we found each pair twice


def test_q1():
    assert q1("test.txt", 64) == 1
    assert q1("test.txt", 40) == 2
    assert q1("test.txt", 38) == 3
    assert q1("data.txt", 100) == 1263


def test_q2():
    assert q2("test.txt", 76) == 3
    assert q2("test.txt", 74) == 7
    assert q2("test.txt", 70) == 41
    assert q2("data.txt", 100) == 957831
