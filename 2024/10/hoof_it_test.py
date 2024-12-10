# Hoof It - https://adventofcode.com/2024/day/10

from collections import deque, defaultdict


def get_data(filename: str) -> dict[tuple[int, int], int]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    topomap = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            topomap[y, x] = int(c)

    return topomap


def q1(filename: str) -> int:
    topomap = get_data(filename)
    trailheads = defaultdict(set)
    result = 0
    seen = set()
    q = deque([])

    for pos, val in topomap.items():
        if val == 9:
            trailheads[pos].add(pos)
            q.append((pos, val))

    while q:
        pos, val = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)

        if val == 0:
            result += len(trailheads[pos])
            continue

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + dy, pos[1] + dx)

            if topomap.get(new_pos, -1) == val - 1:
                trailheads[new_pos].update(trailheads[pos])
                q.append((new_pos, val - 1))

    return result


def q2(filename: str) -> int:
    topomap = get_data(filename)
    trailheads = defaultdict(int)
    result = 0
    seen = set()
    q = deque([])

    for pos, val in topomap.items():
        if val == 9:
            trailheads[pos] = 1
            q.append((pos, val))

    while q:
        pos, val = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)

        if val == 0:
            result += trailheads[pos]
            continue

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + dy, pos[1] + dx)

            if topomap.get(new_pos, -1) == val - 1:
                trailheads[new_pos] += trailheads[pos]
                q.append((new_pos, val - 1))

    return result


def test_q1():
    assert q1("test.txt") == 36
    assert q1("data.txt") == 574


def test_q2():
    assert q2("test.txt") == 81
    assert q2("data.txt") == 1238
