from collections import deque


def read_data(filename: str) -> frozenset[tuple]:
    with open(filename) as f:
        return frozenset(tuple(map(int, line.strip().split(','))) for line in f.readlines())


PATTERN = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def generate_cloud(cubes: frozenset[tuple]) -> set[tuple]:
    limits = []
    for i in range(3):
        values = [cube[i] for cube in cubes]
        limits.append((min(values) - 1, max(values) + 1))

    q = deque([(limits[0][0], limits[1][0], limits[2][0])])

    cloud = set()

    while q:
        air = q.popleft()
        for dx, dy, dz in PATTERN:
            new_air = (air[0] + dx, air[1] + dy, air[2] + dz)

            if not (limits[0][0] <= new_air[0] <= limits[0][1]
                    and limits[1][0] <= new_air[1] <= limits[1][1]
                    and limits[2][0] <= new_air[2] <= limits[2][1]):
                continue

            if (new_air not in cloud) and (new_air not in cubes):
                cloud.add(new_air)
                q.append(new_air)

    return cloud


def count_surfaces(filename: str) -> (int, int):
    cubes = read_data(filename)
    outside_air = generate_cloud(cubes)
    result1 = result2 = 0

    for cube in cubes:
        for dx, dy, dz in PATTERN:
            if (cube[0] + dx, cube[1] + dy, cube[2] + dz) not in cubes:
                result1 += 1
            if (cube[0] + dx, cube[1] + dy, cube[2] + dz) in outside_air:
                result2 += 1

    print(f"{result1=} {result2=}")
    return result1, result2


if __name__ == "__main__":
    assert count_surfaces("example.txt") == (64, 58)
    assert count_surfaces("data.txt") == (3530, 2000)
