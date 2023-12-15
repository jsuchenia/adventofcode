#!/usr/bin/env python


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()

def is_shape_valid(cave, elems):
    return all(not (x < 0 or x > 6 or y < 0 or (x, y) in cave) for x, y in elems)

ROCKS = [
    lambda sx, sy: [(sx, sy), (sx + 1, sy), (sx + 2, sy), (sx + 3, sy)],
    lambda sx, sy: [(sx + 1, sy), (sx, sy + 1), (sx + 1, sy + 1), (sx + 2, sy + 1), (sx + 1, sy + 2)],
    lambda sx, sy: [(sx, sy), (sx + 1, sy), (sx + 2, sy), (sx + 2, sy + 1), (sx + 2, sy + 2)],
    lambda sx, sy: [(sx, sy), (sx, sy + 1), (sx, sy + 2), (sx, sy + 3)],
    lambda sx, sy: [(sx, sy), (sx + 1, sy), (sx, sy + 1), (sx + 1, sy + 1)],
]

def simul_cave(filename, i) -> int:
    moves = read_data(filename)

    cave = set()
    highest = move_idx = rock_idx = -1

    stats = {}

    while i > 0:
        rock = ROCKS[rock_idx := (rock_idx + 1) % len(ROCKS)]
        x, y = 2, highest + 4

        while True:
            move = moves[move_idx := (move_idx + 1) % len(moves)]
            nx = x + 1 if move == ">" else x - 1

            if is_shape_valid(cave, rock(nx, y)):
                x = nx

            if is_shape_valid(cave, rock(x, ny := y - 1)):
                y = ny
            else:
                break

        i -= 1

        for e in rock(x, y):
            highest = max(highest, e[1])
            cave.add(e)

        # Stats for part II but also speedup part I
        stats_id = (move_idx, rock_idx)
        if stats_id in stats:
            old_i, old_highest = stats[stats_id]
            diff_i = old_i - i

            if i % diff_i == 0:  # Only for final estimation as cave will be invalid
                factor = i // diff_i
                highest += factor * (highest - old_highest)
                return highest + 1

        stats[stats_id] = i, highest

    return highest + 1

def test_simul_cave_p1_example():
    assert simul_cave("example.txt", 2022) == 3068

def test_simul_cave_p1_data():
    assert simul_cave("data.txt", 2022) == 3161

def test_simul_cave_p2_example():
    assert simul_cave("example.txt", 1_000_000_000_000) == 1_514_285_714_288

def test_simul_cave_p2_data():
    assert simul_cave("data.txt", 1_000_000_000_000) == 1_575_931_232_076
