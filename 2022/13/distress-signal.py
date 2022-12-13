#!/usr/bin/env python
import json
import math


def read_data(filename: str) -> list:
    with open(filename) as f:
        pairs = [pair.split("\n") for pair in f.read().split("\n\n")]
    return [(json.loads(pair[0]), json.loads(pair[1])) for pair in pairs]


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

    print(f"p1 {filename=} {statuses=}")
    result = sum(status[0] for status in statuses if status[1])
    print(f"p1 {filename=} {result=}")
    return result


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
    packets.sort(key=lambda pair: comparator(pair))

    extra_positions = [packets.index(element) + 1 for element in extra_packets]
    print(f"p2 {filename=} {extra_positions=}")
    result = math.prod(extra_positions)
    print(f"p2 {filename=} {result=}")

    return result


if __name__ == "__main__":
    assert p1("example.txt") == 13
    assert p1("data.txt") == 5605

    assert p2("example.txt") == 140
    assert p2("data.txt") == 24969
