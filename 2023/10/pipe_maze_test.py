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

    def is_valid(cell) -> bool:
        x, y = cell
        if not 0 <= y <= len(data):
            return False
        if not 0 <= x <= len(data[0].strip()):
            return False
        return True

    distances = dict()
    distances[start] = 0
    q = deque()
    q.append(start)

    while q:
        cell = q.popleft()
        for next_cell in connections[cell]:
            if is_valid(next_cell) and next_cell not in distances:
                distances[next_cell] = distances[cell] + 1
                q.append(next_cell)
    return max(distances.values())


def q2(filename: str) -> int:
    data = get_data(filename)

    return 0


def test_q1():
    assert q1("test.txt") == 8
    assert q1("data.txt") == 6927


def test_q2():
    assert q2("test2.txt") == 8
    # assert q2("test3.txt") == 10
    # q2("data.txt")
