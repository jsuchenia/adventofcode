# Monkey Market - https://adventofcode.com/2024/day/22
from collections import defaultdict
from itertools import pairwise
from multiprocessing import Pool


def get_data(filename: str) -> list[int]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return [int(line) for line in lines]


def calc_secrets(n: int) -> list[int]:
    result = [n]
    for i in range(2000):
        n ^= (n << 6) & 0xFFFFFF  # ((n * 64) ^ n) % 16777216
        n ^= (n >> 5) & 0xFFFFFF  # ((n // 32) ^ n) % 16777216
        n ^= (n << 11) & 0xFFFFFF  # ((n * 2048) ^ n) % 16777216
        result.append(n)
    return result


def calc_patterns(n: int) -> dict[tuple[int, ...], int]:
    nums = calc_secrets(n)
    patterns = {}
    nums_10 = [n % 10 for n in nums]
    diffs = [n2 - n1 for n1, n2 in pairwise(nums_10)]

    for i in range(len(diffs) - 4):
        if (pattern := tuple(diffs[i:i + 4])) not in patterns:
            patterns[pattern] = nums_10[i + 4]
    return patterns


def q1(filename: str) -> int:
    return sum(calc_secrets(n)[-1] for n in get_data(filename))


def q2(filename: str) -> int:
    all_patterns = defaultdict(int)

    # Similar speed to the below, but uses all cores
    for p in Pool().imap(calc_patterns, get_data(filename)):
        for k, v in p.items():
            all_patterns[k] += v

    # for n in get_data(filename):
    #     for pattern, val in patterns(n).items():
    #         all_patterns[pattern] += val

    return max(all_patterns.values())


def test_q1():
    assert q1("test.txt") == 37327623
    assert q1("test2.txt") == 37990510
    assert q1("data.txt") == 12664695565


def test_q2():
    assert q2("test.txt") == 24
    assert q2("test2.txt") == 23
    assert q2("data.txt") == 1444
