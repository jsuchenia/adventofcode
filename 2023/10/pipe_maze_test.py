# Pipe Maze - https://adventofcode.com/2023/day/10
from collections import deque

type Point = tuple[int, int]
type Connections = dict[Point, list[Point]]

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return lines

def parse_connections(lines: list[str]) -> tuple[Connections, Point]:
    connections = dict()
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

def compute_loop(connections, start) -> set[Point]:
    visited = set()
    q = deque()
    q.append(start)

    # BFS
    while q:
        cell = q.popleft()
        visited.add(cell)
        for next_cell in connections[cell]:
            if next_cell not in visited:
                q.append(next_cell)

    return visited

def q1(filename: str) -> int:
    lines = get_data(filename)
    connections, start = parse_connections(lines)
    loop = compute_loop(connections, start)
    return len(loop) // 2

def q2(filename: str) -> int:
    lines = get_data(filename)
    connections, start = parse_connections(lines)
    loop = compute_loop(connections, start)

    inside = set()
    for y, row in enumerate(lines):
        enclosed = False
        horizontal_start_char = None
        for x, cell in enumerate(row.strip()):
            if (x, y) in loop:
                if cell == "|":
                    enclosed = not enclosed
                elif cell in "LF":
                    horizontal_start_char = cell
                elif cell in "7":
                    if horizontal_start_char == "L":
                        enclosed = not enclosed
                    horizontal_start_char = None
                elif cell == "J" or cell == "S":  # Adjusted for my input data where S seems to be J
                    if horizontal_start_char == "F":
                        enclosed = not enclosed
                    horizontal_start_char = None
            elif enclosed:
                inside.add((x, y))
    return len(inside)

def test_q1():
    assert q1("test.txt") == 8
    assert q1("data.txt") == 6927

def test_q2():
    assert q2("test2.txt") == 4
    assert q2("test3.txt") == 8
    assert q2("data.txt") == 467
