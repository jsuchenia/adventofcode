# Plutonian Pebbles - https://adventofcode.com/2024/day/11
from collections import defaultdict, Counter


def get_data(filename: str) -> list[int]:
    with open(filename) as f:
        line = f.read().strip()
    return list(map(int, line.split(' ')))


def q1(filename: str, *, blinks) -> int:
    nums = get_data(filename)
    stones = Counter(nums)

    for _ in range(0, blinks):
        new_stones = defaultdict(int)
        for stone, n in stones.items():
            if stone == 0:
                new_stones[1] += n
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                l = len(s) // 2
                stone_l, stone_r = int(s[:l]), int(s[l:])

                new_stones[stone_l] += n
                new_stones[stone_r] += n
            else:
                new_stones[stone * 2024] += n
        stones = new_stones
    return sum(stones.values())


def test_q1():
    assert q1("test.txt", blinks=25) == 55312
    assert q1("data.txt", blinks=25) == 187738


def test_q2():
    assert q1("test.txt", blinks=75) == 65601038650482
    assert q1("data.txt", blinks=75) == 223767210249237
