# Haunted Wasteland - https://adventofcode.com/2023/day/8
import re


def get_data(filename: str) -> tuple[str, dict[str, tuple[str, str]]]:
    with open(filename) as f:
        lines = f.read().splitlines()
    steps = lines[0]
    camel_map = {}
    for line in lines[2:]:
        m = re.match(r"^(\w{3}) = \((\w{3}), (\w{3})\)", line)
        if m.groups():
            camel_map[m[1]] = (m[2], m[3])
    return steps, camel_map


def q1(filename: str) -> int:
    steps, cmap = get_data(filename)

    count = 0
    curr = "AAA"
    while True:
        step = steps[count % len(steps)]
        count += 1
        curr = cmap[curr][0] if step == "L" else cmap[curr][1]
        if curr == "ZZZ":
            break
    return count


def q2(filename: str) -> int:
    data = get_data(filename)

    return 0


def test_q1():
    assert q1("test.txt") == 2
    assert q1("test2.txt") == 6
    assert q1("data.txt") == 24253


def test_q2():
    q2("test.txt")
