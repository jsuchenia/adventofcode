# Snowverload - https://adventofcode.com/2023/day/25
from math import prod

from networkx import Graph, minimum_edge_cut, connected_components

def get_data(filename: str) -> Graph:
    g = Graph()
    with open(filename) as f:
        for line in f.read().strip().splitlines():
            name, elements = line.split(": ")

            for element in elements.split():
                g.add_edge(name, element)
    return g

def q1(filename: str) -> int:
    g = get_data(filename)
    g.remove_edges_from(minimum_edge_cut(g))
    return prod(len(c) for c in connected_components(g))

def test_q1():
    assert q1("test.txt") == 54
    assert q1("data.txt") == 531437
