# Cosmic Expansion - https://adventofcode.com/2023/day/11
from itertools import combinations

type Point = tuple[int, int]

def get_data(filename: str) -> set[Point]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return {(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "#"}

def expand_galaxy(galaxy: set[Point], scaling_factor: int) -> set[Point]:
    all_x = {x for x, y in galaxy}
    all_y = {y for x, y in galaxy}

    empty_x = [x for x in range(max(all_x)) if x not in all_x]
    empty_y = [y for y in range(max(all_y)) if y not in all_y]

    def expand(x: int, y: int) -> Point:
        dx = len([ex for ex in empty_x if ex < x])
        dy = len([ey for ey in empty_y if ey < y])
        return x + dx * (scaling_factor - 1), y + dy * (scaling_factor - 1)

    return {expand(x, y) for x, y in galaxy}

def distance(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def q1(filename: str) -> int:
    galaxy = get_data(filename)
    galaxy = expand_galaxy(galaxy, scaling_factor=2)

    distances = [distance(p1, p2) for p1, p2 in combinations(galaxy, 2)]
    return sum(distances)

def q2(filename: str, scaling_factor: int) -> int:
    galaxy = get_data(filename)
    galaxy = expand_galaxy(galaxy, scaling_factor=scaling_factor)

    distances = [distance(p1, p2) for p1, p2 in combinations(galaxy, 2)]
    return sum(distances)

def test_q1():
    assert q1("test.txt") == 374
    assert q1("data.txt") == 9445168

def test_q2():
    assert q2("test.txt", scaling_factor=10) == 1030
    assert q2("test.txt", scaling_factor=100) == 8410
    assert q2("test.txt", scaling_factor=1_000_000) == 82000210

    assert q2("data.txt", scaling_factor=1_000_000) == 742305960572
