#!/usr/bin/env python
import math

def read_data(filename: str) -> list:
    with open(filename) as f:
        pairs = [pair.split("\n") for pair in f.read().split("\n\n")]
    return [(eval(pair[0]), eval(pair[1])) for pair in pairs]

def check_equal(left, right) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left != right:
            return left < right
    elif isinstance(left, list) and isinstance(right, list):
        left_len = len(left)
        right_len = len(right)

        for idx in range(max(left_len, right_len)):
            if idx < left_len and idx < right_len:
                r = check_equal(left[idx], right[idx])
                if r is not None:
                    return r
            else:
                return idx >= left_len
    elif isinstance(left, int):
        return check_equal([left], right)
    else:
        return check_equal(left, [right])

def p1(filename: str) -> int:
    pairs = read_data(filename)
    statuses = [(idx + 1, check_equal(pair[0], pair[1])) for idx, pair in enumerate(pairs)]

    return sum(status[0] for status in statuses if status[1])

class Comparator:
    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return check_equal(self.obj, other.obj)

def p2(filename: str) -> int:
    extra_packets = [[[2]], [[6]]]

    pairs = read_data(filename)
    packets = [packet for pair in pairs for packet in pair]
    packets += extra_packets
    packets.sort(key=lambda pair: Comparator(pair))

    extra_positions = [packets.index(element) + 1 for element in extra_packets]
    return math.prod(extra_positions)

def test_distress_signal_p1_example():
    assert p1("example.txt") == 13

def test_distress_signal_p1_data():
    assert p1("data.txt") == 5605

def test_distress_signal_p2_example():
    assert p2("example.txt") == 140

def test_distress_signal_p2_data():
    assert p2("data.txt") == 24969
