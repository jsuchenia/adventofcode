# Parabolic Reflector Dish - https://adventofcode.com/2023/day/14
import pytest

type Rock = tuple[int, int]

def get_data(filename: str) -> dict[Rock, str]:
    with open(filename) as f:
        return {(x, y): c
                for y, line in enumerate(f.read().strip().splitlines())
                for x, c in enumerate(line)
                if c != '.'}

def move_rocks(cube_shaped: frozenset[Rock], rounded: frozenset[Rock], size: int, direction: Rock):
    while True:
        new_rounded = set()
        for x, y in rounded:
            nx, ny = x + direction[0], y + direction[1]
            if not (0 <= nx <= size and 0 <= ny <= size):
                new_rounded.add((x, y))
            elif (nx, ny) in rounded or (nx, ny) in cube_shaped:
                new_rounded.add((x, y))
            else:
                new_rounded.add((nx, ny))

        if new_rounded == rounded:
            break
        rounded = new_rounded

    return frozenset(rounded)

def q1(filename: str) -> int:
    platform = get_data(filename)
    size = max(max(x, y) for x, y in platform)

    cube_shaped = frozenset(k for k, v in platform.items() if v == "#")
    rounded_rocks = frozenset(k for k, v in platform.items() if v == "O")

    rounded_rocks = move_rocks(cube_shaped, rounded_rocks, size, (0, -1))
    return sum(size - y + 1 for x, y in rounded_rocks)

def q2(filename: str, rounds=1_000_000_000) -> int:
    platform = get_data(filename)
    size = max(max(x, y) for x, y in platform)

    cube_shaped = frozenset(k for k, v in platform.items() if v == "#")
    rounded_rocks = frozenset(k for k, v in platform.items() if v == "O")

    state = {}
    while rounds > 0:
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, size, (0, -1))
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, size, (-1, 0))
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, size, (0, 1))
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, size, (1, 0))
        rounds -= 1

        if rounded_rocks in state and rounds % (state[rounded_rocks] - rounds) == 0:
            break
        state[rounded_rocks] = rounds

    return sum(size - y + 1 for x, y in rounded_rocks)

@pytest.mark.parametrize("filename, result", [("test.txt", 136), ("data.txt", 113424)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 64), ("data.txt", 96003)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
