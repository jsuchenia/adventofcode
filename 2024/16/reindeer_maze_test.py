# Reindeer Maze - https://adventofcode.com/2024/day/16

from networkx import DiGraph, all_shortest_paths, shortest_path_length

from aoclib import *


def get_data(filename: str) -> dict[complex, str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return parse_map(lines, skip_chars="#")


def build_graph(filename):
    area = get_data(filename)

    g = DiGraph()
    start = end = None

    for point, val in area.items():
        if val == 'S':
            start = (point, E)  # From rules
        elif val == 'E':
            end = (point, N)  # N is for all the tasks - hardcoding

        for direction in DIRECTIONS_4:
            if (point + direction) in area:
                g.add_edge((point, direction), (point + direction, direction), weight=1)

            for rotation in (-1j, 1j):
                new_direction = direction * rotation
                if (point + new_direction) in area:
                    g.add_edge((point, direction), (point, new_direction), weight=1000)

    print(f"Grid stats {len(g.nodes)=} {len(g.edges)=}")
    return g, start, end


def simplify_graph(g: DiGraph) -> None:
    for node in list(g.nodes):
        if g.degree(node) == 2 and len(edges := list(g.edges(node))) == 2:
            weight = sum(g.get_edge_data(*edge)['weight'] for edge in edges)
            g.add_edge(edges[0][1], edges[1][1], weight=weight)
            g.remove_node(node)

    print(f"Simplified grid stats {len(g.nodes)=} {len(g.edges)=}")


def q1(filename: str) -> int:
    grid, start, end = build_graph(filename)
    simplify_graph(grid)
    return shortest_path_length(grid, start, end, weight="weight")


def q2(filename: str) -> int:
    grid, start, end = build_graph(filename)
    simplify_graph(grid)

    seats = set()
    for path in all_shortest_paths(grid, start, end, weight="weight"):
        seats.update(point[0] for point in path)

    return len(seats)


def test_q1():
    assert q1("test.txt") == 7036
    assert q1("test2.txt") == 11048
    assert q1("data.txt") == 95476


def test_q2():
    assert q2("test.txt") == 45
    assert q2("test2.txt") == 64
    assert q2("data.txt") == 511
