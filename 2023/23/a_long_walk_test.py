# A Long Walk - https://adventofcode.com/2023/day/23
from collections import deque

import pytest
from networkx import DiGraph, Graph, all_simple_paths, path_weight

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
    visited = set()
    while q:
        node = q.popleft()
        if node in visited:
            continue
        visited.add(node)
        for edge in g.edges(node):
            distance = 1
            measured = {node}
            target = edge[1]
            while True:
                target_edges = g.edges(target)
                target_nodes = {n[1] for n in target_edges}
                filtered_nodes = target_nodes - measured
                if len(filtered_nodes) != 1:
                    break
                distance += 1
                measured.add(target)
                target = filtered_nodes.pop()
            if target:
                # print(f"{node=} -> {target=} {distance=}")
                ng.add_edge(node, target, distance=distance)
                if target not in visited:
                    q.append(target)
    return ng

def q1(filename: str) -> int:
    g, start, end = get_data(filename, directions=DIRECTIONS_q1)
    wg = convert_to_weighted(g, start)
    paths = all_simple_paths(wg, start, end)
    return max(path_weight(wg, path, weight='distance') for path in paths)

def q2(filename: str) -> int:
    g, start, end = get_data(filename, directions=DIRECTIONS_q2)
    wg = convert_to_weighted(g, start)
    paths = all_simple_paths(wg, start, end)
    return max(path_weight(wg, path, weight='distance') for path in paths)

def test_q1():
    assert q1("test.txt") == 94
    assert q1("data.txt") == 2354

@pytest.mark.skip("1 minute - can be improved..")
def test_q2():
    assert q2("test.txt") == 154
    assert q2("data.txt") == 6686
