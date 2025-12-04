# Printing Department - https://adventofcode.com/2025/day/4

from aoclib import parse_map, neighbors_8


def get_data(filename: str) -> dict[complex, str]:
    with open(filename) as f:
        grid = parse_map(f.readlines(), skip_chars=" .\n")
    return grid


def q1(filename: str) -> int:
    grid = get_data(filename)
    count = 0
    for p in grid.keys():
        if grid[p] != '@':
            continue
        if len([grid[n] for n in neighbors_8(p) if n in grid and grid[n] == '@']) < 4:
            count += 1
    return count


def q2(filename: str) -> int:
    grid = get_data(filename)
    count = 0
    while True:
        removed = False
        for p in grid.keys():
            if grid[p] != '@':
                continue
            if len([grid[n] for n in neighbors_8(p) if n in grid and grid[n] == '@']) < 4:
                grid[p] = 'X'
                count += 1
                removed = True
        if not removed:
            break
    # print_map(grid)
    return count


def test_q1():
    assert q1("test.txt") == 13
    assert q1("data.txt") == 1553


def test_q2():
    assert q2("test.txt") == 43
    assert q2("data.txt") == 8442
