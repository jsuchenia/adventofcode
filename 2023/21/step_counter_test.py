# Step Counter - https://adventofcode.com/2023/day/21
from collections import deque

import pytest
from matplotlib import pyplot as plt

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

def get_start(lines):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                return x, y
    raise ValueError("No start point")

def q1(filename: str, steps) -> int:
    lines = get_data(filename)
    assert len(lines) == len(lines[0])  # It's a square

    # start is always (len(lines)//2, len(lines)//2)
    # in q1 it will never reach a border
    start = get_start(lines)
    assert start == (len(lines) // 2, len(lines) // 2)

    def is_valid(xc, yc):
        # Q2 optimisation, not important in Q1
        # In q1 steps < len(lines) // 2
        return lines[yc % len(lines)][xc % len(lines[0])] != '#'

    visited = set()
    q = deque([(start[0], start[1], steps)])

    while q:
        x, y, step = state = q.popleft()
        if state in visited:
            continue
        visited.add(state)

        if step == 0:
            continue

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if not is_valid(nx := x + dx, ny := y + dy):
                continue
            q.append((nx, ny, step - 1))
    return sum(1 for v in visited if v[2] == 0)

def q2(filename="data.txt", steps=26501365) -> int:
    data = get_data(filename)
    # From wolfram alpha: 26501365 and 131 - no relations, only 26501365 = 202300 × 131 + 65

    size = len(data)
    n = steps // size  # 202300 - we have samples, each with 131 step
    p = steps % size  # 65 - also magic value as it's a half of a size of a grid

    val0 = q1(filename, steps=p)  # 3742
    val1 = 33564  # q1(filename, steps=1 * size + p)  # 33564 (~2 sec)
    val2 = 93148  # q1(filename, steps=2 * size + p)  # 93148 (~13 sec)
    val3 = 182494  # q1(filename, steps=3 * size + p)  # 182494 (~3 minutes...)
    # val202300 - target
    print(f"{val0=} {val1=} {val2=} {val3=}")

    diff1 = val1 - val0  # 29822
    diff2 = val2 - val1  # 59584 = val0 + 1*ddiff
    diff3 = val3 - val2  # 89346 = val0 + 2*ddiff
    print(f"DIFF {val1=} {diff1=} {diff2=} {diff3=}")

    ddiff1 = diff2 - diff1  # 29762
    ddiff2 = diff3 - diff2  # 29762 # BINGO!!
    print(f"DIFF OF DIFF {ddiff1=} {ddiff2=}")

    # assert ddiff1 == ddiff2
    # assert diff3 - diff1 == 2 * ddiff1

    # diff = 29762*x + 29822
    # Linear function of delta (where x is per each 131 block - value is a real value)

    def diff(x):
        for i in range(x):
            yield i * ddiff1 + diff1

    return sum(diff(n)) + val0

def test_q1():
    assert q1("test.txt", 6) == 16
    assert q1("data.txt", 64) == 3682

def test_q1_nostrict():
    assert q1("test.txt", 6) == 16
    assert q1("test.txt", 10) == 50
    assert q1("test.txt", 50) == 1594
    assert q1("test.txt", 100) == 6536
    # too complex to simulate..
    # assert q1("test.txt", 500) == 167004
    # assert q1("test.txt", 1000) == 668697
    # assert q1("test.txt", 5000) == 16733044

@pytest.mark.skip
def test_q2_data_nostrict(filename="data.txt", steps=26501365):
    data = get_data(filename)

    size = len(data)
    n = steps // size  # 202300
    p = steps % size  # 65

    assert q1("data.txt", steps=p) == 3742  # 96ms
    assert q1("data.txt", steps=1 * size + p) == 33564  # 2sec 380ms
    assert q1("data.txt", steps=2 * size + p) == 93148  # 13 sec 135ms
    assert q1("data.txt", steps=3 * size + p) == 182494  # (3 minutes...)

@pytest.mark.skip
def test_plot_points():
    q1_points = [(6, 16), (10, 50), (50, 1594), (100, 6536), (500, 167004), (1000, 668697), (5000, 16733044)]

    x = [p[0] for p in q1_points]
    y = [p[1] for p in q1_points]

    # for p1, p2 in pairwise(q1_points):
    #     print(f"{p1=} {p2=}")
    #     diffx = p2[0] - p1[0]
    #     diffy = p2[1] - p1[1]
    #     print(f"{diffx=} {diffy=}")
    #     delta = diffy / diffx
    #     print(f"{delta=}")
    #
    # deltas = [(p2[1] - p1[1] / p2[0] - p1[0], p2[0] - p1[0]) for p1, p2 in pairwise(q1_points)]
    # for d1, d2 in pairwise(deltas):
    #     diffx = d2[0] - d1[0]
    #     diffy = d2[1] - d1[1]
    #     print(f"{diffx=} {diffy=}")
    #     ddiff = diffy / diffx
    #     print(f"{ddiff=}")

    plt.plot(x, y)
    plt.grid(True)
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.savefig("test.txt.png")

def test_q2():
    assert q2() == 609012263058042
