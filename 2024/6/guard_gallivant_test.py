# Guard Gallivant - https://adventofcode.com/2024/day/6

N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)

DIRECTIONS = [N, E, S, W]


def get_data(filename: str) -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    area = {}
    start = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            area[(y, x)] = char
            if char == "^":
                start = (y, x)
    assert start is not None

    return area, start


def simul_guard(area: dict[tuple[int, int], str], position: tuple[int, int]) -> set[tuple[int, int]]:
    direction = 0
    visited = {position}
    while True:
        y, x = position
        dy, dx = DIRECTIONS[direction]
        new_position = (y + dy, x + dx)
        if new_position not in area:
            break

        if area[new_position] == '.' or area[new_position] == '^':
            visited.add(new_position)
            position = new_position
            continue
        elif area[new_position] == '#':
            direction = (direction + 1) % len(DIRECTIONS)
            continue
        else:
            raise ValueError("Something is wrong with a data")

    return visited


def q1(filename: str) -> int:
    return len(simul_guard(*get_data(filename)))


def is_a_loop(area: dict[tuple[int, int], str], position: tuple[int, int]) -> bool:
    direction = 0
    visited = {(position, direction)}
    while True:
        y, x = position
        dy, dx = DIRECTIONS[direction]
        new_position = (y + dy, x + dx)
        if new_position not in area:
            return False

        if (new_position, direction) in visited:
            return True

        if area[new_position] == '.' or area[new_position] == '^':
            visited.add((new_position, direction))
            position = new_position
            continue
        elif area[new_position] == '#':
            direction = (direction + 1) % len(DIRECTIONS)
            continue
        else:
            raise ValueError("Something is wrong with a data")


def q2(filename: str) -> int:
    area, start_position = get_data(filename)
    potential_positions = simul_guard(area, start_position)
    res = 0

    for obstacle in potential_positions:
        area[obstacle] = '#'
        if is_a_loop(area, start_position):
            res += 1

        area[obstacle] = '.'

    return res


def test_q1():
    assert q1("test.txt") == 41
    assert q1("data.txt") == 4663


def test_q2():
    assert q2("test.txt") == 6
    assert q2("data.txt") == 1530
