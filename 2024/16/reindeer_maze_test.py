# Reindeer Maze - https://adventofcode.com/2024/day/16

import networkx as nx

from aoclib import *


def get_data(filename: str) -> dict[complex, str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return parse_map(lines)


def build_graph(filename):
    area = get_data(filename)

    g = nx.DiGraph()
    start = None
    end = None

    for point, val in area.items():
        if val == '#':
            continue
        if val == 'S':
            start = (point, E)  # From rules
        if val == 'E':
            end = (point, N)  # N is for all the tasks - hardcoding

        for direction in DIRECTIONS_4:
            g.add_node((point, direction))
            if area.get((point + direction)) != '#':
                g.add_edge((point, direction), (point + direction, direction), weight=1)

            for rotation in (-1j, 1j):
                new_direction = direction * rotation
                if area.get((point + new_direction)) != '#':
                    g.add_edge((point, direction), (point, new_direction), weight=1000)

    print(f"Grid stats {len(g.nodes)=} {len(g.edges)=}")
    return g, start, end


def q1(filename: str) -> int:
    g, start, end = build_graph(filename)

    return nx.shortest_path_length(g, start, end, weight="weight")


def q2(filename: str) -> int:
    grid, start, end = build_graph(filename)

    seats = set()
    for path in nx.all_shortest_paths(grid, start, end, weight="weight"):
        print(f"Current seats... {len(seats)=}")
        for point in path:
            seats.add(point[0])

    return len(seats)


def test_q1():
    assert q1("test.txt") == 7036
    assert q1("test2.txt") == 11048
    assert q1("data.txt") == 95476


def test_q2():
    assert q2("test.txt") == 45
    assert q2("test2.txt") == 64
    assert q2("data.txt") == 511
