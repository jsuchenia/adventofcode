# The Floor Will Be Lava - https://adventofcode.com/2023/day/16
from collections import deque, defaultdict

import pytest

type Point = tuple[int, int]
type Grid = tuple[dict[Point, str], int, int]

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

def get_data(filename: str) -> Grid:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
        grid = {}
        for y, line in enumerate(lines):
            for x, chr in enumerate(line):
                grid[(x, y)] = chr
        return grid, len(lines[0]), len(lines)

def count_energy(start: Point, direction: Point, data: Grid, ) -> int:
    grid, max_x, max_y = data

    def is_valid(p: Point) -> bool:
        if not 0 <= p[0] < max_x:
            return False
        if not 0 <= p[1] < max_y:
            return False
        return True

    q = deque([(start, direction)])
    visited = defaultdict(set)

    while q:
        point, direction = q.popleft()
        if not is_valid(point) or direction in visited[point]:
            continue

        visited[point].add(direction)
        c = grid[point]

        def new_point(d: Point) -> tuple[Point, Point]:
            return (point[0] + d[0], point[1] + d[1]), d

        if c == '.':
            q.append(new_point(direction))
        elif c == '/':
            if direction == E:
                q.append(new_point(N))
            elif direction == W:
                q.append(new_point(S))
            elif direction == N:
                q.append(new_point(E))
            else:
                q.append(new_point(W))
        elif c == '\\':
            if direction == E:
                q.append(new_point(S))
            elif direction == W:
                q.append(new_point(N))
            elif direction == N:
                q.append(new_point(W))
            else:
                q.append(new_point(E))
        elif c == "|":
            if direction == W or direction == E:
                q.append(new_point(N))
                q.append(new_point(S))
            else:
                q.append(new_point(direction))
        elif c == "-":
            if direction == N or direction == S:
                q.append(new_point(E))
                q.append(new_point(W))
            else:
                q.append(new_point(direction))
        else:
            raise ValueError(f"Wrong c {c} at position {new_point}")

    return len(visited)

def q1(filename: str) -> int:
    return count_energy((0, 0), E, get_data(filename))

def q2(filename: str) -> int:
    _, max_x, max_y = grid = get_data(filename)

    results = [count_energy((x, 0), S, grid) for x in range(max_x)]
    results += [count_energy((x, max_y - 1), N, grid) for x in range(max_x)]
    results += [count_energy((0, y), E, grid) for y in range(max_y)]
    results += [count_energy((max_x - 1, y), W, grid) for y in range(max_y)]

    return max(results)

@pytest.mark.parametrize("filename, result", [("test.txt", 46), ("data.txt", 6883)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 51), ("data.txt", 7228)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
