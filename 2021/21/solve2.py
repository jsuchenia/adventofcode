#!/usr/local/bin/python3
import re
from itertools import product
from functools import cache, lru_cache

DICE_VALS = [1, 2, 3]
ALL_VALS=[sum(p) for p in product(DICE_VALS, DICE_VALS, DICE_VALS)]

def parse(data):
    res = re.compile("Player (\d+) starting position: (\d+)")
    return res.findall(data)

@cache
def doRun(pos1, pos2, sum1=0, sum2=0):
    # We simulate move only player 0, swapping them after that
    print("Checking with params", pos1, pos2, sum1, sum2)

    wins = [0, 0]
    for s in ALL_VALS:
        newpos = ((pos1 + s - 1 ) % 10) + 1
        newsum = sum1 + newpos

        if newsum >=21:
            wins[0] += 1
        else:
            win2, win1 = doRun(pos2, newpos, sum2, newsum)
            wins[0] += win1
            wins[1] += win2

    print("Win results", wins)
    return wins


def ex2(data):
    startPositions = parse(data)
    positions = [int(p[1]) for p in startPositions]

    res = doRun(positions[0], positions[1])
    print(doRun.cache_info())

    print("Result is", res)
    m = max(res)
    print("Max is", m)
    return m

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    # assert ex2(test) == 444356092776315
    assert ex2(data) == 568867175661958
