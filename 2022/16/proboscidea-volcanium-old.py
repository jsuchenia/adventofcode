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
        paths_len = len(paths)
        result = max(paths[idx1][1] + paths[idx2][1]
                     for idx1 in range(0, paths_len)
                     for idx2 in range(idx1, paths_len)
                     if set(paths[idx1][0]).isdisjoint(paths[idx2][0]))
        print(f"P2: Result is {result=}")
        return result


if __name__ == "__main__":
    assert Simul("example.txt").p1() == 1651
    assert Simul("data.txt").p1() == 1754
    assert Simul("example.txt").p2() == 1707
    assert Simul("data.txt").p2() == 2474

    # Stats on my computer
    # P1: Result is result=1651
    # P1: Result is result=1754
    # P2: Result is result=1707
    # P2: Result is result=2474
    #
    # real    4m49.692s
    # user    4m46.992s
    # sys     0m2.013s
