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
    def simul_p1(self, current: str, remaining_valves: frozenset, time_left: int) -> int:
        current_emit = time_left * self.graph[current][0]
        results = [current_emit]

        for node in remaining_valves:
            distance_moving = self.distances[(current, node)]
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
        print(f"P1: Result is {result=} P1:{self.simul_p1.cache_info()}")
        return result

    def p2(self):
        valves_to_open = frozenset([key for key, value in self.graph.items() if value[0] > 0])

        result = self.simul_p2("AA", valves_to_open, 26)
        print(f"P2: Result is {result=} P1:{self.simul_p1.cache_info()} P2:{self.simul_p2.cache_info()}")
        return result

def test_cave_simulation_p1_example():
    assert Simul("example.txt").p1() == 1651

def test_cave_simulation_p1_data():
    assert Simul("data.txt").p1() == 1754

def test_cave_simulation_p2_example():
    assert Simul("example.txt").p2() == 1707

def test_cave_simulation_p2_data():
    assert Simul("data.txt").p2() == 2474

    # P1: Result is result=1651 P1:CacheInfo(hits=415, misses=402, maxsize=None, currsize=402)
    # P1: Result is result=1754 P1:CacheInfo(hits=53053, misses=77873, maxsize=None, currsize=77873)
    # P2: Result is result=1707 P1:CacheInfo(hits=54677, misses=79445, maxsize=None, currsize=79445) P2:CacheInfo(hits=386, misses=389, maxsize=None, currsize=389)
    # P2: Result is result=2474 P1:CacheInfo(hits=5553755, misses=2522769, maxsize=None, currsize=2522769) P2:CacheInfo(hits=13053, misses=26745, maxsize=None, currsize=26745)
    #
    # real    0m17.324s
    # user    0m16.815s
    # sys     0m0.456s
