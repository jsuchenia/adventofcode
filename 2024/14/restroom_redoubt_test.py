# Restroom Redoubt - https://adventofcode.com/2024/day/14
from collections import defaultdict, deque
from math import prod

from aoclib import *


def get_data(filename: str) -> list[tuple[int, ...]]:
    result = []
    with open(filename) as f:
        for line in f.read().strip().splitlines():
            result.append(ints(line))
        return result


def calc_safety_factor(robots: list[tuple], X: int, Y: int) -> int:
    mid_x, mid_y = X // 2, Y // 2
    q = defaultdict(int)
    for x, y, _, _ in robots:
        if x < mid_x and y < mid_y:
            q[0] += 1
        elif x > mid_x and y < mid_y:
            q[1] += 1
        elif x < mid_x and y > mid_y:
            q[2] += 1
        elif x > mid_x and y > mid_y:
            q[3] += 1

    return prod(q.values())


def q1(filename: str, X: int, Y: int) -> int:
    robots = get_data(filename)

    for _ in range(100):
        for idx, robot in enumerate(robots):
            x, y, dx, dy = robot
            robots[idx] = ((x + dx) % X, (y + dy) % Y, dx, dy)
    return calc_safety_factor(robots, X, Y)


def print_area(area, X, Y):
    print(f"\n\n============================== AREA ======================================")
    for y in range(Y):
        print(''.join('X' if (y + x * 1j) in area else '.' for x in range(X)))
    print(f"==================================== END =====================================\n")


def count_greatest_area(area: dict[complex, str]) -> int:
    seen = set()
    max_area = 0

    for start in area:
        if start in seen:
            continue
        size = 0
        q = deque([start])
        while q:
            pos = q.popleft()
            if pos in seen:
                continue

            size += 1
            for neighbour in neighbors_4(pos):
                if neighbour in area and neighbour not in seen:
                    q.append(neighbour)
            seen.add(pos)
        max_area = max(size, max_area)
    return max_area


def q2(filename: str, X, Y) -> int:
    robots = get_data(filename)
    total = len(robots)

    min_safety = None

    for tick in range(1, 10_000):
        area = dict()
        for idx, robot in enumerate(robots):
            x, y, dx, dy = robot
            x, y = (x + dx) % X, (y + dy) % Y
            robots[idx] = (x, y, dx, dy)
            area[(y + x * 1j)] = "#"

        # Alternative option found later - there are no duplicates on a final image (so total == area len)
        if total == len(area):
            print_area(area, X, Y)
            return tick

        # From https://www.youtube.com/watch?v=uj7OnaBDCiY - safety of a picture with a tree is a minimum
        # safety = calc_safety_factor(robots, X, Y)
        # if min_safety is None or safety < min_safety[0]:
        #     min_safety = (safety, tick)
        #     print(f"{min_safety}")

        # if (gs := count_greatest_area(area)) > 20:
        #     safety = calc_safety_factor(robots, X, Y)
        #     print(f"\n{total=} {len(area)=} {gs=} {tick=} {safety=}")
        #     print_area(area, X, Y)
        #
        #     # img = get_map_as_img(area, footer=f"{tick}/10.000")
        #     # img.save("visualization-tree.png")
        #     return tick
    return min_safety[1]


def test_q1():
    assert q1("test.txt", 11, 7) == 12
    assert q1("data.txt", 101, 103) == 224438715


def test_q2():
    assert q2("data.txt", 101, 103) == 7603
