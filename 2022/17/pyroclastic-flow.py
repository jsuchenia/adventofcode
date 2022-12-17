#!/usr/bin/env python

def ROCK1(sx, sy):
    return [(sx, sy), (sx + 1, sy), (sx + 2, sy), (sx + 3, sy)]


def ROCK2(sx, sy):
    return [(sx + 1, sy), (sx, sy + 1), (sx + 1, sy + 1), (sx + 2, sy + 1), (sx + 1, sy + 2)]


def ROCK3(sx, sy):
    return [(sx, sy), (sx + 1, sy), (sx + 2, sy), (sx + 2, sy + 1), (sx + 2, sy + 2)]


def ROCK4(sx, sy):
    return [(sx, sy), (sx, sy + 1), (sx, sy + 2), (sx, sy + 3)]


def ROCK5(sx, sy):
    return [(sx, sy), (sx + 1, sy), (sx, sy + 1), (sx + 1, sy + 1)]


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def is_shape_valid(cave, elems):
    for x, y in elems:
        if x < 0 or x > 6:
            return False
        if y < 0:
            return False
        if (x, y) in cave:
            return False
    return True


def simul_cave(filename, limit) -> int:
    moves = read_data(filename)

    cave = set()
    highest = -1
    move_idx = -1
    rock_idx = -1
    rocks = [ROCK1, ROCK2, ROCK3, ROCK4, ROCK5]
    stats = {}
    i = limit

    while i > 0:
        rock_idx = (rock_idx + 1) % len(rocks)
        rock = rocks[rock_idx]
        x, y = 2, highest + 4

        while True:
            move_idx = (move_idx + 1) % len(moves)
            move = moves[move_idx]
            if move == '>':
                nx = x + 1
            elif move == '<':
                nx = x - 1
            else:
                raise ValueError(f"Wrong input data!")

            if is_shape_valid(cave, rock(nx, y)):
                x = nx

            ny = y - 1
            if is_shape_valid(cave, rock(x, ny)):
                y = ny
            else:
                break

        i -= 1
        new_highest = highest

        for e in rock(x, y):
            new_highest = max(new_highest, e[1])
            cave.add(e)

        diff_highest = new_highest - highest
        highest = new_highest

        # Stats for part II but also speedup part I
        stats_id = (move_idx, rock_idx, diff_highest)
        if stats_id in stats:
            old_i, old_highest = stats[stats_id]
            diff_i = old_i - i
            diff_highest = highest - old_highest

            if i % diff_i == 0:  # Only for final estimation as cave will be invalid
                factor = i // diff_i
                gain = factor * diff_highest
                highest += gain
                result = highest + 1

                print(f"Estimated result {result=}")
                return result
        stats[stats_id] = i, highest

    result = highest + 1
    print(f"Result {result=}")
    return result


if __name__ == "__main__":
    assert simul_cave("example.txt", limit=2022) == 3068
    assert simul_cave("data.txt", limit=2022) == 3161

    assert simul_cave("example.txt", limit=1_000_000_000_000) == 1_514_285_714_288
    assert simul_cave("data.txt", limit=1_000_000_000_000) == 1_575_931_232_076
