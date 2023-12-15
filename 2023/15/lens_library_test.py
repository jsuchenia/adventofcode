# Lens Library - https://adventofcode.com/2023/day/15
from collections import defaultdict

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().split(',')

def HASH(s: str) -> int:
    h = 0
    for chr in s:
        h = ((h + ord(chr)) * 17) % 256
    return h

def q1(filename: str) -> int:
    return sum(HASH(s) for s in get_data(filename))

def q2(filename: str) -> int:
    # Since python 3.7 built-in dict keeps an order of an insertion
    # https://docs.python.org/3/library/collections.html#ordereddict-objects

    boxes = defaultdict(dict)
    for s in get_data(filename):
        match s.strip('-').split('='):
            case [label, value]:
                boxes[HASH(label)][label] = int(value)
            case [label]:
                boxes[HASH(label)].pop(label, None)

    return sum(
        (box + 1) * idx * value
        for box, lenses in boxes.items()
        for idx, value in enumerate(lenses.values(), start=1))

def test_hash():
    assert HASH("HASH") == 52

def test_q1():
    assert q1("test.txt") == 1320
    assert q1("data.txt") == 507291

def test_q2():
    assert q2("test.txt") == 145
    assert q2("data.txt") == 296921
