# Step Counter - https://adventofcode.com/2023/day/21
from collections import deque
from datetime import datetime

import pytest
from matplotlib import pyplot as plt

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
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
    # From wolfram alpha: 26501365 and 131 - no relations, only 26501365 = 202300 * 131 + 65

    size = len(data)
    n = steps // size  # 202300 - 2023*100 - probably some clue - we have samples, each with 131 step
    p = steps % size  # 65 - also magic value as it's a half of a size of a grid

    val0 = 3742  # q1(filename, steps=p)  # 3742
    val1 = 33564  # q1(filename, steps=1 * size + p)  # 33564 (~2 sec)
    val2 = 93148  # q1(filename, steps=2 * size + p)  # 93148 (~13 sec)
    val3 = 182494  # q1(filename, steps=3 * size + p)  # 182494 (~3 minutes...)
    val4 = 301602  # From WA

    # val202300 - target
    # print(f"{val0=} {val1=} {val2=} {val3=} {val4=}")

    diff1 = val1 - val0  # 29822
    diff2 = val2 - val1  # 59584 = val0 + 1*ddiff
    diff3 = val3 - val2  # 89346 = val0 + 2*ddiff
    diff4 = val4 - val3  # 119108 = val0 + 3*ddiff
    # print(f"DIFF {val1=} {diff1=} {diff2=} {diff3=} {diff4=}")

    ddiff1 = diff2 - diff1  # 29762
    ddiff2 = diff3 - diff2  # 29762 # BINGO!!
    ddiff3 = diff4 - diff3  # 29762 # BINGO!!
    # print(f"DIFF OF DIFF {ddiff1=} {ddiff2=}")

    assert ddiff1 == ddiff2
    assert ddiff2 == ddiff3
    assert diff3 - diff1 == 2 * ddiff1
    assert diff4 - diff1 == 3 * ddiff1

    # diff = 29762*x + 29822
    # Linear function of delta (where x is per each 131 block - value is a real value)

    def diff(x):
        for i in range(x):
            yield i * ddiff1 + diff1

    return sum(diff(n)) + val0

def q2_wa(filename="data.txt", steps=26501365) -> int:
    data = get_data(filename)
    size = len(data)
    n = steps // size

    # Math proposed by WA from 4 samples: https://www.wolframalpha.com/input?i=3742%2C33564%2C93148%2C182494
    # WA is indexing elements from 1, so we have to calculate it for n+1

    wa = lambda x: 14881 * x ** 2 - 14821 * x + 3682
    return wa(n + 1)

def test_q1():
    assert q1("test.txt", 6) == 16
    assert q1("data.txt", 64) == 3682

def test_q2_example_values():
    assert q1("test.txt", 6) == 16
    assert q1("test.txt", 10) == 50
    assert q1("test.txt", 50) == 1594
    assert q1("test.txt", 100) == 6536
    # too complex to simulate on my laptop
    # assert q1("test.txt", 500) == 167004
    # assert q1("test.txt", 1000) == 668697
    # assert q1("test.txt", 5000) == 16733044

def test_q2():
    assert q2() == 609012263058042
    assert q2_wa() == 609012263058042

@pytest.mark.skip("Used to generate samples for a discovery..")
def test_q2_data(filename="data.txt", steps=26501365):
    data = get_data(filename)

    size = len(data)
    p = steps % size  # 65

    # Fastest one was i5 2GHz - timings from that computer
    assert q1("data.txt", steps=p) == 3742  # 96ms
    assert q1("data.txt", steps=1 * size + p) == 33564  # 2sec 380ms
    assert q1("data.txt", steps=2 * size + p) == 93148  # 7 sec
    assert q1("data.txt", steps=3 * size + p) == 182494  # (1 minute...)
    assert q1("data.txt", steps=4 * size + p) == 301602  # (2 minutes...)
    assert q1("data.txt", steps=5 * size + p) == 450472  # (4 minutes...)
    assert q1("data.txt", steps=6 * size + p) == 629104  # (7 minutes...)
    assert q1("data.txt", steps=7 * size + p) == 837498  # (12 minutes...)

@pytest.mark.skip("Used during work on p2")
def test_plot_points():
    # Note:
    # Later investigation proved that those points can form quadratic function - without first two elements
    # https://www.wolframalpha.com/input?i=quadratic+fit+%7B%7B50%2C1594%7D%2C%7B100%2C6536%7D%2C%7B500%2C167004%7D%2C%7B1000%2C668697%7D%2C%7B5000%2C16733044%7D%7D
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

# Compare different CPUs to get data faster
# Fastest one was i5 Macbook PRO 2Ghz - Python 3.12.1 - 8 samples in less than 20 minutes
# Second was Macbook Air M2 - Python 3.12.1
# Third one - Server with Xenon 1.6GHz - but with Python 3.5
def q2_gen(filename="data.txt", steps=26501365):
    lines = get_data(filename)
    size = len(lines)
    start = (len(lines) // 2, len(lines) // 2)

    def is_valid(xc, yc):
        return lines[yc % len(lines)][xc % len(lines[0])] != '#'

    p = steps % size

    visited = set()
    q = deque([(start[0], start[1], 0)])
    results = []
    target = p
    last_step = 0

    while q:
        x, y, step = state = q.popleft()

        if step > target:
            results.append(len(visited))
            now = datetime.now()
            print(f"{now} {target=} {results=}")
            target += size

        if step > last_step:
            visited.clear()
            last_step = step

        if state in visited:
            continue
        visited.add(state)

        if step > last_step:
            visited[last_step].clear()
            last_step = step

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if not is_valid(nx := x + dx, ny := y + dy):
                continue
            q.append((nx, ny, step + 1))

# if __name__ == "__main__":
#     q2_gen()
