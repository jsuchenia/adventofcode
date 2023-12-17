# Clumsy Crucible - https://adventofcode.com/2023/day/17

import networkx as nx

def solve(filename: str, min_n: int, max_n: int) -> int:
    with open(filename) as f:
        data = [[int(n) for n in line.strip()] for line in f.read().splitlines()]

    max_y = len(data)
    max_x = len(data[0])

    def is_valid(x: int, y: int) -> bool:
        if not 0 <= x < max_x:
            return False
        if not 0 <= y < max_y:
            return False
        return True

    graph = nx.DiGraph()
    for y in range(max_y):
        for x in range(max_x):
            src_H = (x, y, "H")
            src_V = (x, y, "V")

            costs = [0, 0, 0, 0]
            for delta in range(1, max_n + 1):
                if is_valid(x + delta, y):
                    costs[0] += data[y][x + delta]
                    if delta >= min_n:
                        graph.add_edge(src_H, (x + delta, y, "V"), weight=costs[0])
                if is_valid(x - delta, y):
                    costs[1] += data[y][x - delta]
                    if delta >= min_n:
                        graph.add_edge(src_H, (x - delta, y, "V"), weight=costs[1])
                if is_valid(x, y + delta):
                    costs[2] += data[y + delta][x]
                    if delta >= min_n:
                        graph.add_edge(src_V, (x, y + delta, "H"), weight=costs[2])
                if is_valid(x, y - delta):
                    costs[3] += data[y - delta][x]
                    if delta >= min_n:
                        graph.add_edge(src_V, (x, y - delta, "H"), weight=costs[3])

    graph.add_edge("start", (0, 0, "H"), weight=0)
    graph.add_edge("start", (0, 0, "V"), weight=0)
    graph.add_edge((max_x - 1, max_y - 1, "H"), "end", weight=0)
    graph.add_edge((max_x - 1, max_y - 1, "V"), "end", weight=0)

    return nx.shortest_path_length(graph, source="start", target="end", weight="weight")

def q1(filename: str) -> int:
    return solve(filename, min_n=0, max_n=3)

def q2(filename: str) -> int:
    return solve(filename, min_n=4, max_n=10)

def test_q1():
    assert q1("test.txt") == 102
    assert q1("data.txt") == 1076

def test_q2():
    assert q2("test.txt") == 94
    assert q2("data.txt") == 1219
