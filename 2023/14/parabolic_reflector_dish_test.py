# Parabolic Reflector Dish - https://adventofcode.com/2023/day/14

type Rock = tuple[int, int]

def get_data(filename: str) -> dict[Rock, str]:
    with open(filename) as f:
        return {(x, y): c
                for y, line in enumerate(f.read().splitlines())
                for x, c in enumerate(line)
                if c != '.'}

def move_rocks(cube_shaped: frozenset[Rock], rounded: frozenset[Rock], max_rows: int, max_cols: int, direction: Rock):
    while True:
        new_rounded = set()
        for x, y in rounded:
            rock = nx, ny = x + direction[0], y + direction[1]
            if not (0 <= nx <= max_cols and 0 <= ny <= max_rows):
                new_rounded.add((x, y))
            elif rock in rounded or rock in cube_shaped:
                new_rounded.add((x, y))
            else:
                new_rounded.add(rock)

        if new_rounded == rounded:
            break
        rounded = new_rounded

    return frozenset(rounded)

def q1(filename: str) -> int:
    platform = get_data(filename)
    max_rows = max(y for x, y in platform)
    max_cols = max(x for x, y in platform)

    cube_shaped = frozenset(k for k, v in platform.items() if v == "#")
    rounded_rocks = frozenset(k for k, v in platform.items() if v == "O")

    rounded_rocks = move_rocks(cube_shaped, rounded_rocks, max_rows, max_cols, (0, -1))
    return sum(max_rows - y + 1 for x, y in rounded_rocks)

def q2(filename: str, rounds=1_000_000_000) -> int:
    platform = get_data(filename)
    max_rows = max(y for x, y in platform)
    max_cols = max(x for x, y in platform)

    cube_shaped = frozenset(k for k, v in platform.items() if v == "#")
    rounded_rocks = frozenset(k for k, v in platform.items() if v == "O")

    state = {}
    while rounds > 0:
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, max_rows, max_cols, (0, -1))
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, max_rows, max_cols, (-1, 0))
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, max_rows, max_cols, (0, 1))
        rounded_rocks = move_rocks(cube_shaped, rounded_rocks, max_rows, max_cols, (1, 0))
        rounds -= 1

        if rounded_rocks in state and rounds % (state[rounded_rocks] - rounds) == 0:
            break
        state[rounded_rocks] = rounds

    return sum(max_rows - y + 1 for x, y in rounded_rocks)

def test_q1():
    assert q1("test.txt") == 136
    assert q1("data.txt") == 113424

def test_q2():
    assert q2("test.txt") == 64
    assert q2("data.txt") == 96003
