# Clumsy Crucible - https://adventofcode.com/2023/day/17

from networkx import DiGraph, shortest_path_length

def solve(filename: str, min_n: int, max_n: int) -> int:
    with open(filename) as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    data = {(x, y): int(n) for y, line in enumerate(lines) for x, n in enumerate(line)}
    max_y = len(lines)
    max_x = len(lines[0])

    graph = DiGraph()
    for x, y in data.keys():
        costs = [0] * 4
        for idx, (dx, dy, d) in enumerate([(1, 0, "V"), (-1, 0, "V"), (0, -1, "H"), (0, 1, "H")]):
            for delta in range(1, max_n + 1):
                if not (nx := x + dx * delta, ny := y + dy * delta) in data:
                    break
                costs[idx] += data[(nx, ny)]
                if delta < min_n:
                    continue
                graph.add_edge((x, y, "H" if d == "V" else "V"), (nx, ny, d), weight=costs[idx])

    graph.add_edge("start", (0, 0, "H"), weight=0)
    graph.add_edge("start", (0, 0, "V"), weight=0)
    graph.add_edge((max_x - 1, max_y - 1, "H"), "end", weight=0)
    graph.add_edge((max_x - 1, max_y - 1, "V"), "end", weight=0)

    return shortest_path_length(graph, source="start", target="end", weight="weight")

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
