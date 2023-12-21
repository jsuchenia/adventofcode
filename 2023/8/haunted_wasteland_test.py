# Haunted Wasteland - https://adventofcode.com/2023/day/8
import math
import re
from itertools import cycle

type CMap = dict[str, tuple[str, str]]

def get_data(filename: str) -> tuple[str, CMap]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    camel_map = {}
    for line in lines[2:]:
        dst, left, right = re.match(r"^(\w{3}) = \((\w{3}), (\w{3})\)", line).groups()
        camel_map[dst] = (left, right)

    return lines[0], camel_map

def simulate(steps: str, cmap: CMap, curr: str, end: str) -> int:
    for idx, step in enumerate(cycle(steps), start=1):
        curr = cmap[curr][0] if step == "L" else cmap[curr][1]
        if re.match(end, curr):
            return idx

def q1(filename: str) -> int:
    steps, cmap = get_data(filename)
    return simulate(steps, cmap, "AAA", "ZZZ")

def q2(filename: str) -> int:
    steps, cmap = get_data(filename)
    starts = [key for key in cmap.keys() if re.match(r"..A", key)]

    # Data was prepared in this way, that length from start -> first "..Z" node is then a cycle
    # We can simplify it to just one result (we don't have to find out a full cycle length with all interim steps)
    # https://www.reddit.com/r/adventofcode/comments/18dfpub/2023_day_8_part_2_why_is_spoiler_correct/

    simulations = [simulate(steps, cmap, start, r"..Z") for start in starts]
    return math.lcm(*simulations)

def test_q1():
    assert q1("test.txt") == 2
    assert q1("test2.txt") == 6
    assert q1("data.txt") == 24253

def test_q2():
    assert q2("test3.txt") == 6
    assert q2("data.txt") == 12357789728873
