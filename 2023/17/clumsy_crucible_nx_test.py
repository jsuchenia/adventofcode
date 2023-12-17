# Clumsy Crucible - https://adventofcode.com/2023/day/17

import networkx as nx

def solve(filename: str, min_n: int, max_n: int) -> int:
    with open(filename) as f:
        lines = [line.strip() for line in f.read().splitlines()]

    data = {(x, y): int(n) for y, line in enumerate(lines) for x, n in enumerate(line)}
    max_y = len(lines)
    max_x = len(lines[0])

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
                for idx, new_point in enumerate([(x + delta, y, "V"), (x - delta, y, "V"), (x, y - delta, "H"), (x, y + delta, "H")]):
                    new_x, new_y, direction = new_point
                    if not is_valid(new_x, new_y):
                        continue
                    costs[idx] += data[(new_x, new_y)]
                    if delta < min_n:
                        continue
                    graph.add_edge(src_H if direction == "V" else src_V, new_point, weight=costs[idx])

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
