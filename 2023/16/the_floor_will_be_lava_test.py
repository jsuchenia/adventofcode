# The Floor Will Be Lava - https://adventofcode.com/2023/day/16
import asyncio
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
        lines = f.read().splitlines()
        grid = {}
        for y, line in enumerate(lines):
            for x, chr in enumerate(line):
                grid[(x, y)] = chr
        return grid, len(lines[0]), len(lines)

async def count_energy(data: Grid, start: Point, direction: Point) -> int:
    grid, max_x, max_y = data

    def is_valid(p: Point) -> bool:
        if not 0 <= p[0] < max_x:
            return False
        if not 0 <= p[1] < max_y:
            return False
        return True

    q = deque()
    q.append((start, direction))
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

async def q1(filename: str) -> int:
    return await count_energy(get_data(filename), (0, 0), E)

async def q2(filename: str) -> int:
    _, max_x, max_y = grid = get_data(filename)

    results = [count_energy(grid, (x, 0), S) for x in range(max_x)]
    results += [count_energy(grid, (x, max_y - 1), N) for x in range(max_x)]
    results += [count_energy(grid, (0, y), E) for y in range(max_y)]
    results += [count_energy(grid, (max_x - 1, y), W) for y in range(max_y)]

    return max(await asyncio.gather(*results))

@pytest.mark.asyncio
async def test_q1():
    assert await q1("test.txt") == 46
    assert await q1("data.txt") == 6883

@pytest.mark.asyncio
async def test_q2():
    assert await q2("test.txt") == 51
    assert await q2("data.txt") == 7228
