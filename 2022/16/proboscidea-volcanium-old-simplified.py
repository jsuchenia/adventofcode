import re
from collections import deque


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
    dist = {}

    for start in graph.keys():
        for end in graph.keys():
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

    def _generate_submoves(self, path: list[str], valves: frozenset[str], emission: int, limit: int):
        current = path[-1]
        for valve in valves:
            distance = self.distances[(current, valve)]
            new_limit = limit - distance - 1
            if new_limit <= 0:
                continue
            new_emission = emission + new_limit * self.graph[valve][0]
            yield from self._generate_submoves(path + [valve], valves - {valve}, new_emission, new_limit)
        yield path, emission

    def generate_moves(self, start, limit):
        for valve in self.valves_to_open:
            distance = self.distances[(start, valve)]
            new_limit = limit - distance - 1
            new_emission = new_limit * self.graph[valve][0]
            yield from self._generate_submoves([valve], self.valves_to_open - {valve}, new_emission, new_limit)

    def p1(self):
        result = max(emission for path, emission in self.generate_moves("AA", 30))
        print(f"P1: Result is {result=}")
        return result

    def p2(self):
        paths = list(self.generate_moves("AA", 26))
        paths_dict = {}

        for path in paths:
            key = frozenset(path[0])
            paths_dict[key] = max(path[1], paths_dict.get(key, 0))

        print(f"P2: Reduction from {len(paths)} vs {len(paths_dict)}")
        result = max(cost1 + cost2
                     for path1, cost1 in paths_dict.items()
                     for path2, cost2 in paths_dict.items()
                     if path1.isdisjoint(path2))
        print(f"    Result is {result=}")
        return result


if __name__ == "__main__":
    assert Simul("example.txt").p1() == 1651
    assert Simul("data.txt").p1() == 1754
    assert Simul("example.txt").p2() == 1707
    assert Simul("data.txt").p2() == 2474

    # real    0m1.730s
    # user    0m1.702s
    # sys     0m0.025s
