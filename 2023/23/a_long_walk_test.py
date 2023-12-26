# A Long Walk - https://adventofcode.com/2023/day/23
from collections import deque
from heapq import heappop, heappush

import pytest
from networkx import DiGraph, Graph, all_simple_edge_paths
from networkx.drawing.nx_agraph import to_agraph

N, S, E, W = (0, -1), (0, 1), (1, 0), (-1, 0)
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
                if is_valid(nx := x + dx, ny := y + dy):
                    g.add_edge((x, y), (nx, ny))

    start, end = (1, 0), (len(lines[0]) - 2, len(lines) - 1)

    assert is_valid(*start)
    assert is_valid(*end)

    return g, start, end

# data.txt converted to 36 nodes only ...
def generate_minor_graph(g: Graph, start) -> Graph:
    """ https://en.wikipedia.org/wiki/Graph_minor """

    ng = DiGraph()  # For q1 we need to stay on DiGraph ...
    q = deque([start])

    while q:
        node = q.popleft()

        for target in g[node].keys():
            measured = {node}

            while len(filtered_nodes := g[target].keys() - measured) == 1:
                measured.add(target)
                target = filtered_nodes.pop()

            if not ng.has_edge(node, target):
                ng.add_edge(node, target, weight=len(measured))
                q.append(target)
    return ng

def q1(filename: str) -> int:
    g, start, end = get_data(filename, directions=DIRECTIONS_q1)
    wg = generate_minor_graph(g, start)
    edge_weights = [sum(wg[a][b]['weight'] for a, b in path) for path in all_simple_edge_paths(wg, start, end)]
    return max(edge_weights)

def q2(filename: str) -> int:
    g, start, end = get_data(filename, directions=DIRECTIONS_q2)
    wg = generate_minor_graph(g, start)

    # Calculate all paths using all_simple_paths - 1min 20sec
    # paths = all_simple_paths(wg, start, end)
    # return max(path_weight(wg, path, weight='weight') for path in paths)

    # Calculate using edge_paths - 53sec
    # edge_weights = [sum(wg[a][b]['weight'] for a, b in path) for path in all_simple_edge_paths(wg, start, end)]
    # return max(edge_weights)

    # Calculate all possible paths manually (with a priority q) - 36sec...
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

@pytest.mark.parametrize("filename, result", [("test.txt", 9), ("data.txt", 36)])
def test_minor(filename: str, result: int):
    g, start, end = get_data(filename, directions=DIRECTIONS_q2)
    wg = generate_minor_graph(g, start)

    assert len(wg.nodes) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 94), ("data.txt", 2354)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.skip("38sec.. too long for CI")
@pytest.mark.parametrize("filename, result", [("test.txt", 154), ("data.txt", 6686)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result

@pytest.mark.skip
def test_visualize_q2():
    g, start, end = get_data("data.txt", directions=DIRECTIONS_q2)
    wg = generate_minor_graph(g, start)
    a = to_agraph(wg)
    a.draw("data-graphviz-q2.png", format="png", prog="fdp")
