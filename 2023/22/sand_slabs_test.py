# Sand Slabs - https://adventofcode.com/2023/day/22
from collections import defaultdict
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Cube:
    x: int
    y: int
    z: int

type Brick = tuple[Cube, Cube]

def get_data(filename: str) -> list[Brick]:
    bricks = []
    with open(filename) as f:
        for line in f.read().strip().splitlines():
            points = line.split("~")
            p1 = Cube(*[int(n) for n in points[0].split(',')])
            p2 = Cube(*[int(n) for n in points[1].split(',')])
            assert p1.x <= p2.x and p1.y <= p2.y and p1.z <= p2.z
            bricks.append((p1, p2))

    bricks.sort(key=lambda b: b[0].z)
    return bricks

def overlap_xy(b1: Brick, b2: Brick) -> bool:
    return max(b1[0].x, b2[0].x) <= min(b1[1].x, b2[1].x) and max(b1[0].y, b2[0].y) <= min(b1[1].y, b2[1].y)

def fall_down(bricks: list[Brick]) -> None:
    for idx, brick in enumerate(bricks):
        max_z = 0
        for other in bricks[:idx]:
            if overlap_xy(brick, other):
                max_z = max(max_z, other[1].z)
        if (dz := brick[0].z - max_z) > 1:
            brick[0].z -= (dz - 1)
            brick[1].z -= (dz - 1)

type SupportDict = dict[Brick, set[Brick]]

def calculate_supports(bricks) -> tuple[SupportDict, SupportDict]:
    supports, supported_by = defaultdict(set), defaultdict(set)

    for idx, brick in enumerate(bricks):
        for other in bricks[:idx]:
            if overlap_xy(brick, other) and other[1].z + 1 == brick[0].z:
                supports[other].add(brick)
                supported_by[brick].add(other)
    return supports, supported_by

def q1(filename: str) -> int:
    bricks = get_data(filename)
    fall_down(bricks)
    supports, supported_by = calculate_supports(bricks)

    result = 0
    for brick in bricks:
        others = supports[brick]
        if len(others) == 0 or all(len(supported_by[other]) > 1 for other in others):
            result += 1
    return result

def q2(filename: str) -> int:
    bricks = get_data(filename)
    fall_down(bricks)
    supports, supported_by = calculate_supports(bricks)

    results = 0
    for idx, brick in enumerate(bricks):
        failing = {brick}

        for other in bricks[idx + 1:]:
            if len(supported_by[other]) > 0 and len(supported_by[other] - failing) == 0:
                failing.add(other)
        if len(failing) > 1:
            results += len(failing) - 1
    return results

def test_q1():
    assert q1("test.txt") == 5
    assert q1("data.txt") == 395

def test_q2():
    assert q2("test.txt") == 7
    assert q2("data.txt") == 64714