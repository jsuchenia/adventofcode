# Laboratories - https://adventofcode.com/2025/day/7
from collections import deque, defaultdict

from aoclib import *


def get_data(filename: str) -> tuple[dict[complex, str], complex]:
    with open(filename) as f:
        grid = parse_map(f.read().strip().splitlines())
    return grid, find_in_map(grid, "S")[0]


def q1(filename: str) -> int:
    grid, start = get_data(filename)
    q = deque([start])
    total = 0

    while q:
        pos = q.popleft()
        total += grid[pos] == '^'
        for child in (pos + SE, pos + SW) if grid[pos] == '^' else (pos + S,):
            if child in grid and child not in q:
                q.append(child)
    return total


def q2(filename: str) -> int:
    grid, start = get_data(filename)
    timelines = defaultdict(int)
    timelines[start] = 1
    q = deque([start])

    while q:
        pos = q.popleft()
        for child in (pos + SE, pos + SW) if grid[pos] == '^' else (pos + S,):
            timelines[child] += timelines[pos]
            if child in grid and child not in q:
                q.append(child)

    return sum([val for pos, val in timelines.items() if pos not in grid])


def test_q1():
    assert q1("test.txt") == 21
    assert q1("data.txt") == 1609


def test_q2():
    assert q2("test.txt") == 40
    assert q2("data.txt") == 12472142047197
