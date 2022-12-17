import re
from collections import deque


# Influenced implementation in C++ where visited path is keep as state as bits, with map of known costs

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
        self.filename = filename
        self.graph = read_data(filename)
        self.distances = build_distance(self.graph)
        self.valves_to_open = frozenset([key for key, value in self.graph.items() if value[0] > 0])
        self.markers = {val: 1 << idx for idx, val in enumerate(self.valves_to_open)}

    def simul(self, pos: str, state: int, time_left: int, score: int, costs_map: dict) -> None:
        for node in self.valves_to_open:
            marker = self.markers[node]
            if state & marker:
                continue

            new_time = time_left - self.distances[(pos, node)] - 1
            if new_time <= 0:
                continue

            new_score = score + new_time * self.graph[node][0]
            new_state = state | marker
            costs_map[new_state] = max(new_score, costs_map.get(new_state, 0))
            self.simul(node, new_state, new_time, new_score, costs_map)

    def p1(self):
        cost_map = {}
        self.simul("AA", 0, 30, 0, cost_map)
        result = max(cost_map.values())
        print(f"P1 {self.filename=}: Result is {result=}")
        return result

    def p2(self):
        cost_map = {}
        self.simul("AA", 0, 26, 0, cost_map)

        result = max(cost1 + cost2 for state1, cost1 in cost_map.items()
                     for state2, cost2 in cost_map.items()
                     if not state1 & state2)

        print(f"P2 {self.filename=}: Result is {result=}")
        return result


if __name__ == "__main__":
    assert Simul("example.txt").p1() == 1651
    assert Simul("data.txt").p1() == 1754
    assert Simul("example.txt").p2() == 1707
    assert Simul("data.txt").p2() == 2474

    # P1 self.filename='example.txt': Result is result=1651
    # P1 self.filename='data.txt': Result is result=1754
    # P2 self.filename='example.txt': Result is result=1707
    # P2 self.filename='data.txt': Result is result=2474
    #
    # real    0m1.452s
    # user    0m1.439s
    # sys     0m0.010s
