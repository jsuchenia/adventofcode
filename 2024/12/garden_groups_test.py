# Garden Groups - https://adventofcode.com/2024/day/12
from collections import deque


def get_data(filename: str) -> dict[tuple[int, int], str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    area = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            area[y, x] = c
    return area


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def q1(filename: str) -> int:
    data = get_data(filename)

    seen = set()
    result = 0
    for pos in data.keys():
        if pos in seen:
            continue

        area = perimeter = 0
        q = deque([pos])
        while q:
            check = q.popleft()
            if check in seen:
                continue
            seen.add(check)
            area += 1
            y, x = check
            for dy, dx in DIRECTIONS:
                new_pos = y + dy, x + dx
                if data[pos] == data.get(new_pos, ""):
                    q.append(new_pos)
                else:
                    perimeter += 1

        # print(f"Area of {data[pos]} with {area=} and {perimeter=}")
        result += area * perimeter

    return result


def q2(filename: str) -> int:
    data = get_data(filename)

    seen = set()
    result = 0
    for pos in data.keys():
        if pos in seen:
            continue

        area = sides = 0
        q = deque([pos])
        while q:
            check = q.popleft()
            if check in seen:
                continue
            seen.add(check)
            area += 1
            y, x = check
            for dy, dx in DIRECTIONS:
                new_pos = y + dy, x + dx
                if data[pos] == data.get(new_pos, ""):
                    q.append(new_pos)

            # Check corners
            for i in range(len(DIRECTIONS)):
                dy1, dx1 = DIRECTIONS[i]
                dy2, dx2 = DIRECTIONS[(i + 1) % len(DIRECTIONS)]
                new_pos1 = y + dy1, x + dx1
                new_pos2 = y + dy2, x + dx2

                # In a correct NESW order, sum of directions will be a correct diagonal direction
                # As there is always one 0 in N, E, S or W
                mid_pos = y + dy1 + dy2, x + dx1 + dx2

                pos1_val = data.get(new_pos1, "")
                pos2_val = data.get(new_pos2, "")
                mid_pos_val = data.get(mid_pos, "")

                if data[pos] != pos1_val and data[pos] != pos2_val:
                    sides += 1  # Outer corner
                elif data[pos] == pos1_val and data[pos] == pos2_val and data[pos] != mid_pos_val:
                    sides += 1  # Inner corner

        # print(f"Area of {data[pos]} with {area=} and {sides=}")
        result += area * sides

    return result


def test_q1():
    assert q1("test1.txt") == 140
    assert q1("test2.txt") == 772
    assert q1("test3.txt") == 1930
    assert q1("data.txt") == 1361494


def test_q2():
    assert q2("test1.txt") == 80
    assert q2("test2.txt") == 436
    assert q2("test3.txt") == 1206
    assert q2("data.txt") == 830516
