from collections import deque

def read_data(filename: str) -> frozenset[tuple]:
    with open(filename) as f:
        return frozenset(tuple(map(int, line.strip().split(","))) for line in f.readlines())

PATTERN = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

def generate_water(cubes: frozenset[tuple]) -> set[tuple]:
    limits = []
    for i in range(3):
        values = [cube[i] for cube in cubes]
        limits.append((min(values) - 1, max(values) + 1))

    q = deque([(limits[0][0], limits[1][0], limits[2][0])])

    water = set()

    while q:
        air = q.popleft()
        for dx, dy, dz in PATTERN:
            pos = (air[0] + dx, air[1] + dy, air[2] + dz)

            if not (limits[0][0] <= pos[0] <= limits[0][1] and limits[1][0] <= pos[1] <= limits[1][1] and limits[2][0] <= pos[2] <= limits[2][1]):
                continue

            if (pos not in water) and (pos not in cubes):
                water.add(pos)
                q.append(pos)

    return water

def count_surfaces(filename: str) -> (int, int):
    cubes = read_data(filename)
    water = generate_water(cubes)
    result1 = result2 = 0

    for cube in cubes:
        for dx, dy, dz in PATTERN:
            if (cube[0] + dx, cube[1] + dy, cube[2] + dz) not in cubes:
                result1 += 1
            if (cube[0] + dx, cube[1] + dy, cube[2] + dz) in water:
                result2 += 1

    return result1, result2

def test_count_surfaces_example():
    assert count_surfaces("example.txt") == (64, 58)

def test_count_surfaces_data():
    assert count_surfaces("data.txt") == (3530, 2000)
