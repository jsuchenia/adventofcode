# Cosmic Expansion - https://adventofcode.com/2023/day/11
from functools import cache
from itertools import combinations

type Point = tuple[int, int]


def get_data(filename: str) -> set[Point]:
    with open(filename) as f:
        lines = f.read().splitlines()

    galaxies = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.add((x, y))
    return galaxies


def expand_galaxy(galaxy: set[Point]) -> set[Point]:
    xs = [x for x, y in galaxy]
    ys = [y for x, y in galaxy]

    empty_x = [x for x in range(max(xs)) if x not in xs]
    empty_y = [y for y in range(max(ys)) if y not in ys]

    @cache
    def expand(x, y):
        dx = len([ex for ex in empty_x if ex < x])
        dy = len([ey for ey in empty_y if ey < y])
        return x + dx, y + dy

    result = set()
    for x, y in galaxy:
        result.add(expand(x, y))

    return result


def distance(p1, p2):
    x = abs(p1[0] - p2[0])
    y = abs(p1[1] - p2[1])

    return x + y


def q1(filename: str) -> int:
    galaxy = get_data(filename)
    galaxy = expand_galaxy(galaxy)

    distances = [distance(p1, p2) for p1, p2 in combinations(galaxy, 2)]
    return sum(distances)


def q2(filename: str) -> int:
    data = get_data(filename)

    return 0


def test_q1():
    assert q1("test.txt") == 374
    assert q1("data.txt") == 9445168


def test_q2():
    q2("data.txt")
