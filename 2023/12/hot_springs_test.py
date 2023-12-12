# Hot Springs - https://adventofcode.com/2023/day/12
from functools import cache


def get_data(filename: str):
    with open(filename) as f:
        results = []
        for line in f.read().splitlines():
            data, nums = line.split()
            nums = tuple([int(n) for n in nums.split(",")])
            results.append((data, nums))

        return results


@cache
def check_line(line: str, nums):
    needed_springs = sum(nums)

    if needed_springs == 0:
        return 1 if "#" not in line else 0

    results = 0
    size = nums[0]
    possible_windows = len(line) - needed_springs + 1  # At least one window

    for i in range(possible_windows):
        before = line[:i]
        window = line[i : i + size]
        after = line[i + size :]

        if "#" in before:
            continue

        if not all(c in "#?" for c in window):
            continue

        if after and after[0] not in ".?":
            continue

        results += check_line(after[1:], nums[1:])

    return results


def q1(filename: str) -> int:
    data = get_data(filename)
    result = 0
    for line, nums in data:
        result += check_line(line, nums)

    return result


def q2(filename: str) -> int:
    data = get_data(filename)
    result = 0
    for line, nums in data:
        line = "?".join([line] * 5)
        nums = nums * 5
        result += check_line(line, nums)

    return result


def test_line():
    assert check_line("???.###", (1, 1, 3)) == 1
    assert check_line(".??..??...?##.", (1, 1, 3)) == 4


def test_q1():
    assert q1("test.txt") == 21
    assert q1("data.txt") == 7379


def test_q2():
    assert q2("test.txt") == 525152
    assert q2("data.txt") == 7732028747925
