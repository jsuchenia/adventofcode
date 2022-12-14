import re


def read_data(filename: str):
    point = re.compile(r"(\d+),(\d+)")
    with open(filename) as f:
        return [[(int(p[0]), int(p[1])) for p in point.findall(line)] for line in f.readlines()]


def build_cave(data: list) -> (set, int):
    cave = set()
    deep = 0

    for line in data:
        for idx in range(len(line) - 1):
            x1, x2 = sorted([line[idx][0], line[idx + 1][0]])
            y1, y2 = sorted([line[idx][1], line[idx + 1][1]])
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    cave.add((x, y))
                    deep = max(deep, y)

    return cave, deep


def simul_sand(filename: str, use_floor: bool) -> int:
    cave, deep = build_cave(read_data(filename))
    amount = 0

    start = (500, 0)
    while True:
        sand = start
        while True:
            if sand[1] <= deep and (sand[0], sand[1] + 1) not in cave:
                sand = (sand[0], sand[1] + 1)
                continue
            if sand[1] <= deep and (sand[0] - 1, sand[1] + 1) not in cave:
                sand = (sand[0] - 1, sand[1] + 1)
                continue
            if sand[1] <= deep and (sand[0] + 1, sand[1] + 1) not in cave:
                sand = (sand[0] + 1, sand[1] + 1)
                continue

            if sand[1] > deep and not use_floor:
                print(f"p1 {filename=} {amount=}")
                return amount

            amount += 1
            cave.add(sand)

            if sand == start:
                print(f"p2 {filename=} {amount=}")
                return amount

            break


if __name__ == "__main__":
    assert simul_sand("example.txt", use_floor=False) == 24
    assert simul_sand("data.txt", use_floor=False) == 843

    assert simul_sand("example.txt", use_floor=True) == 93
    assert simul_sand("data.txt", use_floor=True) == 27625
