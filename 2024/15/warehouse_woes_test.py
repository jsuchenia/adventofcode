# Warehouse Woes - https://adventofcode.com/2024/day/15
from aoclib import *


def get_data(filename: str) -> tuple[dict[Point, str], Point, str]:
    with open(filename) as f:
        data = f.read().strip()

    map, moves = data.split("\n\n")
    area = parse_map(map.splitlines())
    start = [key for key, val in area.items() if val == "@"]

    assert len(start) == 1

    return area, start[0], moves.replace('\n', '')


MOVES = {
    '^': N,
    '>': E,
    'v': S,
    '<': W
}


def q1(filename: str) -> int:
    area, start, moves = get_data(filename)
    for move in moves:
        pos = start
        to_move = [pos]
        direction = MOVES[move]
        while True:
            pos = pos + direction
            val = area[pos]
            if val == 'O':
                to_move.append(pos)
            elif val == '.':
                break
            elif val == '#':
                to_move.clear()
                break
        if to_move:
            for m in reversed(to_move):
                area[m + direction] = area[m]
            area[start] = '.'
            start = start + direction
        # print_map(area)

    return sum(100 * point.y + point.x for point, val in area.items() if val == 'O')


def resize_map(area: dict[Point, str]) -> dict[Point, str]:
    new_area = {}
    for point, val in area.items():
        if val == '#' or val == '.':
            new_area[Point(x=point.x * 2, y=point.y)] = val
            new_area[Point(x=point.x * 2 + 1, y=point.y)] = val
        elif val == '@':
            new_area[Point(x=point.x * 2, y=point.y)] = val
            new_area[Point(x=point.x * 2 + 1, y=point.y)] = '.'
        elif val == 'O':
            new_area[Point(x=point.x * 2, y=point.y)] = '['
            new_area[Point(x=point.x * 2 + 1, y=point.y)] = ']'
        else:
            raise ValueError(f"Wrong value of point {point=} {val=}")

    return new_area


def q2(filename: str) -> int:
    area, start, moves = get_data(filename)
    area, start = resize_map(area), Point(x=2 * start.x, y=start.y)

    for move in moves:
        positions = [start]
        to_move = [start]
        direction = MOVES[move]

        while True:
            next_positions = []
            for point in positions:
                point = point + direction
                val = area[point]
                if val == '[':
                    next_positions.append(point)
                    if direction in (S, N):
                        next_positions.append(point + E)
                elif val == ']':
                    next_positions.append(point)
                    if direction in (S, N):
                        next_positions.append(point + W)
                elif val == '.':
                    continue
                elif val == '#':
                    to_move.clear()
                    break
                else:
                    raise ValueError(f"Wrong value of point {point=} {val=}")

            if next_positions and to_move:
                to_move.extend(next_positions)
                positions = next_positions
                continue
            else:
                break

        if to_move:
            for point in reversed(to_move):
                area[point + direction] = area[point]

            for point in set(to_move) - set(point + direction for point in to_move):
                area[point] = '.'
            start = start + direction
        # print_map(area)

    return sum(100 * point.y + point.x for point, val in area.items() if val == '[')


def test_q1():
    assert q1("test1.txt") == 2028
    assert q1("test2.txt") == 10092
    assert q1("data.txt") == 1421727


def test_q2():
    assert q2("test3.txt") == 618
    assert q2("test2.txt") == 9021
    assert q2("data.txt") == 1463160
