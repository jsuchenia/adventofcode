#!/usr/local/bin/python3
import re
from functools import cache
from itertools import product

DICE_VALS = [1, 2, 3]
ALL_VALS = [sum(p) for p in product(DICE_VALS, repeat=3)]


def parse(data):
    res = re.compile(r"Player (\d+) starting position: (\d+)")
    return res.findall(data)


@cache
def do_run(pos1, pos2, sum1=0, sum2=0):
    # We simulate move only player 0, swapping them after that
    print("Checking with params", pos1, pos2, sum1, sum2)

    wins = [0, 0]
    for s in ALL_VALS:
        new_pos = ((pos1 + s - 1) % 10) + 1
        total = sum1 + new_pos

        if total >= 21:
            wins[0] += 1
        else:
            win2, win1 = do_run(pos2, new_pos, sum2, total)
            wins[0] += win1
            wins[1] += win2

    print(f"Win results {wins=}")
    return wins


def ex2(data):
    start_positions = parse(data)
    positions = [int(p[1]) for p in start_positions]

    res = do_run(positions[0], positions[1])

    print("Result is", res)
    m = max(res)
    print("Max is", m)
    return m


if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    # assert ex2(test) == 444356092776315
    assert ex2(data) == 568867175661958
