# Pipe Maze - https://adventofcode.com/2023/day/10
# From Reddit: https://www.reddit.com/r/adventofcode/comments/18evyu9/comment/kcso138/
#    https://en.wikipedia.org/wiki/Shoelace_formula
#    https://en.wikipedia.org/wiki/Pick%27s_theorem

type MazePoint = tuple[int, int]
type Connections = dict[MazePoint, list[MazePoint]]

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().splitlines()

def parse_connections(lines: list[str]) -> tuple[Connections, MazePoint]:
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

def compute_loop(connections: Connections, start: MazePoint) -> list[MazePoint]:
    point = start
    results = []
    prev_node = None

    while point != start or not prev_node:
        results.append(point)
        next_nodes = [p for p in connections[point] if p != prev_node]
        prev_node, point = point, next_nodes[0]
    return results

def q2(filename: str) -> int:
    lines = get_data(filename)
    connections, start = parse_connections(lines)
    loop = compute_loop(connections, start)

    # Shoelace formula
    s = 0
    for i in range(len(loop)):
        x_1, y_1 = loop[i]
        x_2, y_2 = loop[(i + 1) % len(loop)]
        s += x_1 * y_2 - y_1 * x_2

    area = abs(s / 2)

    # Pick's theorem
    return int(area - len(loop) / 2 + 1)

def test_q2():
    assert q2("test2.txt") == 4
    assert q2("test3.txt") == 8
    assert q2("data.txt") == 467
