# Linen Layout - https://adventofcode.com/2024/day/19
from functools import cache


def get_data(filename: str) -> tuple[list[str], list[str]]:
    with open(filename) as f:
        towels, patterns = lines = f.read().strip().split("\n\n")

    towels = towels.strip().split(',')
    towels = [towel.strip() for towel in towels]
    patterns = patterns.strip().splitlines()
    return towels, patterns


def q1(filename: str) -> int:
    towels, patterns = get_data(filename)
    towels = set(towels)

    print(f"{towels=} {patterns=}")

    @cache
    def check(pattern: str) -> bool:
        for towel in towels:
            if pattern.startswith(towel):
                if not (rest := pattern[len(towel):]) or check(rest):
                    return True
        return False

    return sum(check(pattern) for pattern in patterns)


def q2(filename: str) -> int:
    towels, patterns = get_data(filename)
    towels = set(towels)

    @cache
    def check(pattern: str) -> int:
        result = 0

        for towel in towels:
            if pattern.startswith(towel):
                if rest := pattern[len(towel):]:
                    result += check(rest)
                else:
                    result += 1
        return result

    return sum(check(pattern) for pattern in patterns)


def test_q1():
    assert q1("test.txt") == 6
    assert q1("data.txt") == 358


def test_q2():
    assert q2("test.txt") == 16
    assert q2("data.txt") == 600_639_829_400_603
