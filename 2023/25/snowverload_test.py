# Snowverload - https://adventofcode.com/2023/day/25
from math import prod

import pytest
from networkx import Graph, minimum_edge_cut, connected_components, is_connected
from networkx.drawing.nx_agraph import to_agraph

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
    assert is_connected(g)

    edges = minimum_edge_cut(g)
    g.remove_edges_from(edges)
    assert not is_connected(g)

    return prod(map(len, connected_components(g)))

def test_q1():
    assert q1("test.txt") == 54
    assert q1("data.txt") == 531437

@pytest.mark.skip
def test_graph():
    g = get_data("data.txt")
    a = to_agraph(g)
    a.draw("data-graphviz.png", format="png", prog="sfdp")
