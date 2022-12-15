import re
from collections import deque
from functools import cache


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

    @cache
    def simul_p1(self, pos: str, remaining_valves: frozenset, time_left: int) -> int:
        current_emit = time_left * self.graph[pos][0]
        results = [current_emit]

        for node in remaining_valves:
            distance_moving = self.distances[(pos, node)]
            reach_time = time_left - distance_moving - 1
            new_remaining = remaining_valves - {node}
            if reach_time > 0:
                emitted = self.simul_p1(node, new_remaining, reach_time)
                results.append(current_emit + emitted)

        return max(results)

    @cache
    def simul_p2(self, pos: str, remaining_valves: frozenset, time_left: int) -> int:
        current_emit = time_left * self.graph[pos][0]
        results = [current_emit, current_emit + self.simul_p1("AA", remaining_valves, 26)]

        for node in remaining_valves:
            distance_moving = self.distances[(pos, node)]
            reach_time = time_left - distance_moving - 1
            new_remaining = remaining_valves - {node}
            if reach_time > 0:
                emitted = self.simul_p2(node, new_remaining, reach_time)
                results.append(current_emit + emitted)

        return max(results)

    def p1(self):
        valves_to_open = frozenset([key for key, value in self.graph.items() if value[0] > 0])
        result = self.simul_p1("AA", valves_to_open, 30)
        print(f"P1: Result is {result=} {self.simul_p1.cache_info()}")
        return result

    def p2(self):
        valves_to_open = frozenset([key for key, value in self.graph.items() if value[0] > 0])

        result = self.simul_p2("AA", valves_to_open, 26)
        print(f"P2: Result is {result=} {self.simul_p1.cache_info()} {self.simul_p2.cache_info()}")
        return result


if __name__ == "__main__":
    assert Simul("example.txt").p1() == 1651
    assert Simul("data.txt").p1() == 1754
    assert Simul("example.txt").p2() == 1707
    assert Simul("data.txt").p2() == 2474
