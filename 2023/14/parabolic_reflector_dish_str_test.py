# Parabolic Reflector Dish - https://adventofcode.com/2023/day/14
from copy import deepcopy

import pytest

type Platform = list[list[str]]

def get_data(filename: str) -> Platform:
    with open(filename) as f:
        return list(list(line) for line in f.read().strip().splitlines())

def move(platform: Platform) -> Platform:
    while True:
        result = deepcopy(platform)
        for y, line in enumerate(platform[1:], start=1):
            for x, c in enumerate(line):
                if c == 'O' and platform[y - 1][x] == '.':
                    result[y - 1][x] = 'O'
                    result[y][x] = '.'

        if result == platform:
            return result
        platform = result

def rotate(platform: Platform) -> Platform:
    # clockwise
    return list(list(column[::-1]) for column in zip(*platform))

def q1(filename: str) -> int:
    platform = get_data(filename)
    platform = move(platform)

    return sum((len(platform) - y) * line.count("O") for y, line in enumerate(platform))

def q2(filename: str, rounds=1_000_000_000) -> int:
    platform = get_data(filename)
    state = {}
    while rounds > 0:
        for _ in range(4):
            platform = move(platform)
            platform = rotate(platform)
        rounds -= 1

        data = '\n'.join([''.join(line) for line in platform])
        if data in state and rounds % (state[data] - rounds) == 0:
            break
        state[data] = rounds

    return sum((len(platform) - y) * line.count("O") for y, line in enumerate(platform))

def test_q1():
    assert q1("test.txt") == 136
    assert q1("data.txt") == 113424

@pytest.mark.skip("Took 30 sec on my laptop, set-based took 5sec.")
def test_q2():
    assert q2("test.txt") == 64
    assert q2("data.txt") == 96003
