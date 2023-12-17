# Clumsy Crucible - https://adventofcode.com/2023/day/17
from heapq import heappop, heappush

def get_data(filename: str) -> list[list[int]]:
    with open(filename) as f:
        return [[int(n) for n in line.strip()] for line in f.read().splitlines()]

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

# Dijkstra algorithm - with a limitation about n
# So as a state we keep all params and use cost as a priority
# BTW: heapq is faster than queue.PriorityQueue (twice slower)

def solve(grid, min_n, max_n) -> int:
    visited = set()
    q = [(0, 0, 0, 0, 0, 0)]

    def is_valid(px, py) -> bool:
        if not 0 <= px < len(grid[0]):
            return False
        if not 0 <= py < len(grid):
            return False
        return True

    while q:
        cost, x, y, dx, dy, n = heappop(q)
        if x == len(grid[0]) - 1 and y == len(grid) - 1 and n >= min_n:
            return cost

        state = (x, y, dx, dy, n)
        if state in visited:
            continue
        visited.add(state)

        for nx, ny in [E, S, W, N]:
            if not is_valid(new_x := x + nx, new_y := y + ny):
                continue

            new_cost = cost + grid[new_y][new_x]
            if (nx, ny) == (dx, dy):
                if n < max_n:
                    heappush(q, (new_cost, new_x, new_y, dx, dy, n + 1))

            elif (nx, ny) != (-dx, -dy):
                if n >= min_n or cost == 0:
                    heappush(q, (new_cost, new_x, new_y, nx, ny, 1))

    raise ValueError("No path available")

def q1(filename: str) -> int:
    grid = get_data(filename)
    return solve(grid, min_n=0, max_n=3)

def q2(filename: str) -> int:
    grid = get_data(filename)
    return solve(grid, min_n=4, max_n=10)

def test_q1():
    assert q1("test.txt") == 102
    assert q1("data.txt") == 1076

def test_q2():
    assert q2("test.txt") == 94
    assert q2("data.txt") == 1219
