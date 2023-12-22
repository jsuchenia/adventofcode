# Pipe Maze - https://adventofcode.com/2023/day/10
# Implementation in shapely library - something new
import pytest
from matplotlib import pyplot as plt
from shapely import Point, Polygon

type MazePoint = tuple[int, int]
type Connections = dict[MazePoint, list[MazePoint]]

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().splitlines()

def parse_connections(lines: list[str]) -> tuple[Connections, MazePoint]:
    connections = {}
    start = None
    for y, row in enumerate(lines):
        for x, cell in enumerate(row.strip()):
            if cell == "|":
                connections[(x, y)] = [(x, y - 1), (x, y + 1)]
            elif cell == "-":
                connections[(x, y)] = [(x - 1, y), (x + 1, y)]
            elif cell == "L":
                connections[(x, y)] = [(x, y - 1), (x + 1, y)]
            elif cell == "J":
                connections[(x, y)] = [(x, y - 1), (x - 1, y)]
            elif cell == "7":
                connections[(x, y)] = [(x, y + 1), (x - 1, y)]
            elif cell == "F":
                connections[(x, y)] = [(x, y + 1), (x + 1, y)]
            elif cell == "S":
                start = (x, y)

    connections[start] = [src for src, conn in connections.items() for dst in conn if dst == start]
    return connections, start

def compute_loop(connections: Connections, start: MazePoint) -> list[MazePoint]:
    point = start
    results = []
    prev_node = None

    while point != start or not prev_node:
        results.append(point)
        next_nodes = [p for p in connections[point] if p != prev_node]
        prev_node, point = point, next_nodes[0]
    return results

def q1(filename: str) -> int:
    lines = get_data(filename)
    connections, start = parse_connections(lines)
    points = [Point(p) for p in compute_loop(connections, start)]
    p = Polygon(points)
    return p.boundary.length // 2

def q2(filename: str) -> int:
    lines = get_data(filename)
    connections, start = parse_connections(lines)
    points = [Point(p) for p in compute_loop(connections, start)]
    p = Polygon(points)
    interior = p.area - p.boundary.length / 2 + 1

    # # It takes 55 seconds, but we can check if point is in a polygon
    # interior_points = [(x, y) for y in range(len(lines)) for x in range(len(lines[0])) if p.contains(Point(x, y))]
    # print(f"{len(interior_points)=}")
    return interior

def visualise(filename: str):
    lines = get_data(filename)
    connections, start = parse_connections(lines)
    points = [Point(p) for p in compute_loop(connections, start)]
    p = Polygon(points)

    x, y = p.exterior.xy
    plt.clf()
    plt.xscale('linear')
    plt.yscale('linear')
    plt.title(filename)
    plt.plot(x, y)
    plt.savefig(filename + ".png")

def test_q1():
    assert q1("test.txt") == 8
    assert q1("data.txt") == 6927

def test_q2():
    assert q2("test2.txt") == 4
    assert q2("test3.txt") == 8
    assert q2("data.txt") == 467

@pytest.mark.skip
def test_visualize():
    visualise("test.txt")
    visualise("data.txt")
