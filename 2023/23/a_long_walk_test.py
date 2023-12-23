# A Long Walk - https://adventofcode.com/2023/day/23
from collections import deque
from heapq import heappop, heappush

import pytest
from networkx import DiGraph, Graph, all_simple_paths, path_weight
from networkx.drawing.nx_agraph import to_agraph

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

DIRECTIONS_q1 = {'.': [N, S, E, W], '>': [E], '<': [W], 'v': [S], '^': [N], '#': []}
DIRECTIONS_q2 = {'.': [N, S, E, W], '>': [N, S, E, W], '<': [N, S, E, W], 'v': [N, S, E, W], '^': [N, S, E, W], '#': []}

type Point = tuple[int, int]

def get_data(filename: str, directions) -> tuple[Graph, Point, Point]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    g = DiGraph()

    def is_valid(x, y):
        if not 0 <= x < len(lines[0]):
            return False
        if not 0 <= y < len(lines):
            return False
        return lines[y][x] != '#'

    for y, line in enumerate(lines):
        for x, chr in enumerate(line):
            for dx, dy in directions[chr]:
                nx = x + dx
                ny = y + dy
                if is_valid(nx, ny):
                    g.add_edge((x, y), (nx, ny))

    start = (1, 0)
    end = (len(lines[0]) - 2, len(lines) - 1)
    assert is_valid(*start)
    assert is_valid(*end)

    return g, start, end

# data.txt converted to 36 nodes only..
def convert_to_weighted(g: Graph, start) -> Graph:
    ng = DiGraph()
    q = deque()
    q.append(start)
    while q:
        node = q.popleft()

        for target in g[node]:
            distance = 1
            measured = {node}
            while True:
                target_nodes = g[target].keys()
                filtered_nodes = target_nodes - measured
                if len(filtered_nodes) != 1:
                    break
                distance += 1
                measured.add(target)
                target = filtered_nodes.pop()
            if target:
                # print(f"{node=} -> {target=} {distance=}")
                if not ng.has_edge(node, target) or ng[node][target]['weight'] < distance:
                    ng.add_edge(node, target, weight=distance)
                    if target not in q:
                        q.append(target)
    return ng

def q1(filename: str) -> int:
    g, start, end = get_data(filename, directions=DIRECTIONS_q1)
    wg = convert_to_weighted(g, start)
    paths = all_simple_paths(wg, start, end)
    return max(path_weight(wg, path, weight='weight') for path in paths)

def q2(filename: str) -> int:
    g, start, end = get_data(filename, directions=DIRECTIONS_q2)
    wg = convert_to_weighted(g, start)

    # Calculate all paths using networkx - 1min 20sec
    # paths = all_simple_paths(wg, start, end)
    # return max(path_weight(wg, path, weight='weight') for path in paths)

    # Calculate all possible paths manually- 38sec...
    q = [(0, start, {start}, 0)]
    end_costs = []
    while q:
        _, node, path, cost = heappop(q)

        if node == end:
            end_costs.append(cost)
            continue

        for target in wg[node]:
            if target not in path:
                distance = cost + wg[node][target]['weight']
                heappush(q, (-distance, target, path | {target}, distance))

    return max(end_costs)

def test_q1():
    assert q1("test.txt") == 94
    assert q1("data.txt") == 2354

@pytest.mark.skip("38sec.. too long for CI")
def test_q2():
    assert q2("test.txt") == 154
    assert q2("data.txt") == 6686

@pytest.mark.skip
def test_visualize_q2():
    g, start, end = get_data("data.txt", directions=DIRECTIONS_q2)
    wg = convert_to_weighted(g, start)
    a = to_agraph(wg)
    a.draw("data-graphviz.png", format="png", prog="fdp")
