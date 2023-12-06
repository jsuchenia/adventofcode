import re
from collections import deque

import pytest

# First implementation, based on collections - solved P1 (example + data), P2 for example


def read_data(filename: str) -> dict[str, tuple]:
    id_pattern = re.compile(r" ([A-Z]+)")
    rate_pattern = re.compile(r"rate=(\d+);")
    m = {}

    with open(filename) as f:
        for line in f.readlines():
            ids = id_pattern.findall(line)
            rate = rate_pattern.findall(line)
            m[ids[0]] = (int(rate[0]), ids[1:])

    return m

def get_distance(graph, start, end) -> int:
    q = deque()
    visited = set()
    q.append((0, start))

    while q:
        dist, node = q.popleft()
        visited.add(node)
        for child in graph[node][1]:
            if child == end:
                return dist + 1

            if child not in visited:
                q.append((dist + 1, child))

    raise ValueError(f"Empty queue and not in a graph!")

def build_distance(graph):
    vales_to_open = list(graph.keys())

    dist = {}

    for start in vales_to_open:
        for end in vales_to_open:
            if start != end:
                dist[(start, end)] = dist[(end, start)] = get_distance(graph, start, end)
            else:
                dist[(start, end)] = 0

    return dist

class Simul:
    def __init__(self, filename):
        self.graph = read_data(filename)
        self.distances = build_distance(self.graph)
        self.valves_to_open = frozenset([key for key, value in self.graph.items() if value[0] > 0])

    def generate_moves(self, current: str, path: list[str], remaining_valves: frozenset[str], emission: int, limit: int):
        for valve in remaining_valves:
            distance = self.distances[(current, valve)]
            new_limit = limit - distance - 1
            if new_limit <= 0:
                continue
            new_emission = emission + new_limit * self.graph[valve][0]
            yield from self.generate_moves(valve, path + [valve], remaining_valves - {valve}, new_emission, new_limit)
        yield path, emission

    def p1(self):
        result = max(emission for path, emission in self.generate_moves("AA", [], self.valves_to_open, 0, 30))
        print(f"P1: Result is {result=}")
        return result

    def p2(self):
        paths = list(self.generate_moves("AA", [], self.valves_to_open, 0, 26))
        paths_len = len(paths)
        result = max(
            paths[idx1][1] + paths[idx2][1]
            for idx1 in range(0, paths_len)
            for idx2 in range(idx1, paths_len)
            if set(paths[idx1][0]).isdisjoint(paths[idx2][0])
        )
        print(f"P2: Result is {result=}")
        return result

def test_simul_cave_p1_example():
    assert Simul("example.txt").p1() == 1651

def test_simul_cave_p1_data():
    assert Simul("data.txt").p1() == 1754

def test_simul_cave_p2_example():
    assert Simul("example.txt").p2() == 1707

@pytest.mark.skip(reason="It takes 4 minutes without simplification")
def test_simul_cave_p2_data():
    assert Simul("data.txt").p2() == 2474
