#!/usr/local/bin/python3
import re
from collections import Counter
from functools import cache
from itertools import product

DICE_VALS = [1, 2, 3]
ALL_VALS = [sum(p) for p in product(DICE_VALS, repeat=3)]
ALL_DISTINCT_VALUES = Counter(ALL_VALS).most_common()

def parse(data):
    res = re.compile(r"Player (\d+) starting position: (\d+)")
    return res.findall(data)

@cache
def do_run(my_pos, other_pos, my_sum=0, other_sum=0) -> tuple[int, int]:
    # We simulate move only player 0, swapping them after that
    print(f"Checking with params {my_pos=} {other_pos=} {my_sum=} {other_sum=}")

    my_wins = other_wins = 0
    for s, factor in ALL_DISTINCT_VALUES:
        new_pos = ((my_pos + s - 1) % 10) + 1
        new_sum = my_sum + new_pos

        if new_sum >= 21:
            my_wins += factor
        else:
            win2, win1 = do_run(other_pos, new_pos, other_sum, new_sum)
            my_wins += win1 * factor
            other_wins += win2 * factor

    print(f"Interim results {my_wins=} {other_wins=}")
    return my_wins, other_wins

def ex2(filename):
    data = open(filename, "r").read()
    start_positions = parse(data)
    positions = [int(p[1]) for p in start_positions]

    result = do_run(positions[0], positions[1])

    print(f"Result is {result=}")
    return max(result)

def test_dirac_test():
    assert ex2("test.txt") == 444356092776315

def test_dirac_data():
    assert ex2("data.txt") == 568867175661958
