# Resonant Collinearity - https://adventofcode.com/2024/day/8
from collections import defaultdict
from itertools import combinations


def get_data(filename: str) -> tuple[dict[tuple[int, int], str], dict[tuple[int, int], set[tuple[int, int]]]]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    area = {}
    pairs = defaultdict(set)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            area[(y, x)] = char
            if char != '.':
                pairs[char].add((y, x))

    return area, pairs


def q1(filename: str) -> int:
    area, pairs = get_data(filename)
    found_positions = set()

    for char, positions in pairs.items():
        for pos1, pos2 in combinations(positions, 2):
            new_pos_1 = (2 * pos1[0] - pos2[0], 2 * pos1[1] - pos2[1])
            new_pos_2 = (2 * pos2[0] - pos1[0], 2 * pos2[1] - pos1[1])

            if new_pos_1 in area: found_positions.add(new_pos_1)
            if new_pos_2 in area: found_positions.add(new_pos_2)

    return len(found_positions)


def q2(filename: str) -> int:
    area, pairs = get_data(filename)
    found_positions = set()

    for char, positions in pairs.items():
        for pos1, pos2 in combinations(positions, 2):
            dy, dx = pos2[0] - pos1[0], pos2[1] - pos1[1]

            i = 0
            while True:
                found = False
                for d in [-1, 1]:
                    new_pos = (pos1[0] + d * dy * i, pos1[1] + d * dx * i)
                    if new_pos in area:
                        found_positions.add(new_pos)
                        found = True
                if not found:
                    break
                i += 1
    return len(found_positions)


def test_q1():
    assert q1("test.txt") == 14
    assert q1("data.txt") == 336


def test_q2():
    assert q2("test.txt") == 34
    assert q2("data.txt") == 1131
