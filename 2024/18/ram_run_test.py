# RAM Run - https://adventofcode.com/2024/day/18
from networkx import shortest_path_length, Graph, shortest_path, NetworkXNoPath

from aoclib import *


def get_data(filename: str) -> list[complex]:
    with open(filename) as f:
        nums = [ints(line) for line in f.read().strip().splitlines()]
    return [num[0] + 1j * num[1] for num in nums]


def q1(filename: str, limit: int, end: int) -> int:
    points = set(get_data(filename)[:limit])

    g = Graph()

    for y in range(end + 1):
        for x in range(end + 1):
            if (point := x + 1j * y) not in points:
                g.add_node(point)
                for new_point in neighbors_4(point):
                    if new_point not in points and new_point in g:
                        g.add_edge(point, new_point)

    return shortest_path_length(g, 0, end + end * 1j)


def q2(filename: str, end: int) -> str:
    points = get_data(filename)

    g = Graph()

    for y in range(end + 1):
        for x in range(end + 1):
            g.add_node(point := x + 1j * y)
            for new_point in neighbors_4(point):
                if new_point in g:
                    g.add_edge(point, new_point)

    last_path = set(shortest_path(g, 0, (end_point := end + 1j * end)))
    for point in points:
        g.remove_node(point)
        if point not in last_path:
            continue

        try:
            last_path = set(shortest_path(g, 0, end_point))
        except NetworkXNoPath:
            return f"{int(point.real)},{int(point.imag)}"

    raise ValueError("No such point on a list")


def test_q1():
    assert q1("test.txt", 12, 6) == 22
    assert q1("data.txt", 1024, 70) == 322


def test_q2():
    assert q2("test.txt", 6) == "6,1"
    assert q2("data.txt", 70) == "60,21"
