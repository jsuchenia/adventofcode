# Pipe Maze - https://adventofcode.com/2023/day/10
from collections import defaultdict, deque


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def get_connections(filename: str):
    data = get_data(filename)
    connections = defaultdict(list)
    start = None
    for y, row in enumerate(data):
        for x, cell in enumerate(row.strip()):
            if cell == "|":
                connections[(x, y)].append((x, y - 1))
                connections[(x, y)].append((x, y + 1))
            elif cell == "-":
                connections[(x, y)].append((x - 1, y))
                connections[(x, y)].append((x + 1, y))

            elif cell == "L":
                connections[(x, y)].append((x, y - 1))
                connections[(x, y)].append((x + 1, y))

            elif cell == "J":
                connections[(x, y)].append((x, y - 1))
                connections[(x, y)].append((x - 1, y))

            elif cell == "7":
                connections[(x, y)].append((x, y + 1))
                connections[(x, y)].append((x - 1, y))

            elif cell == "F":
                connections[(x, y)].append((x, y + 1))
                connections[(x, y)].append((x + 1, y))
            elif cell == "S":
                start = (x, y)

    start_connections = []
    for src, conn in connections.items():
        for dst in conn:
            if dst == start:
                start_connections.append(src)

    connections[start] = start_connections

    return connections, start


def q1(filename: str) -> int:
    connections, start = get_connections(filename)

    loop = set()
    q = deque()
    q.append(start)

    while q:
        cell = q.popleft()
        loop.add(cell)
        for next_cell in connections[cell]:
            if next_cell not in loop:
                q.append(next_cell)
    return len(loop) // 2


def q2(filename: str) -> int:
    connections, start = get_connections(filename)

    loop = set()
    q = deque()
    q.append(start)

    while q:
        cell = q.popleft()
        loop.add(cell)
        for next_cell in connections[cell]:
            if next_cell not in loop:
                q.append(next_cell)

    data = get_data(filename)
    inside = set()
    for y, row in enumerate(data):
        enclosed = False
        horizontal_from_up = None
        for x, cell in enumerate(row.strip()):
            if (x, y) in loop:
                if cell == "|":
                    enclosed = not enclosed
                elif cell == "L":
                    horizontal_from_up = True
                elif cell == "F":
                    horizontal_from_up = False
                elif cell in "7":
                    if horizontal_from_up:
                        enclosed = not enclosed
                    horizontal_from_up = None
                elif cell == "J":
                    if not horizontal_from_up:
                        enclosed = not enclosed
                    horizontal_from_up = None
                elif cell == "S":  # In a test data this condition is different
                    enclosed = not enclosed
                    horizontal_from_up = None
            else:
                if enclosed:
                    # print((x, y))
                    inside.add((x, y))

    print(f"{len(inside)=}")
    return len(inside)


def test_q1():
    assert q1("test.txt") == 8
    assert q1("data.txt") == 6927


def test_q2():
    # assert q2("test2.txt") == 4
    # assert q2("test3.txt") == 8
    assert q2("data.txt") == 467
