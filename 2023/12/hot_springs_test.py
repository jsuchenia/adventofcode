# Hot Springs - https://adventofcode.com/2023/day/12
from functools import cache

def get_data(filename: str):
    with open(filename) as f:
        results = []
        for line in f.read().splitlines():
            data, nums = line.split()
            nums = tuple(int(n) for n in nums.split(","))
            results.append((data, nums))

        return results

@cache
def check_line(line: str, nums):
    if (needed_springs := sum(nums)) == 0:
        return 0 if "#" in line else 1

    results, block_size = 0, nums[0]
    needed_dots = len(nums) - 1
    # possible_windows = len(line) - block_size + 1
    possible_windows = len(line) - needed_springs - needed_dots + 1  # At least one block
    for i in range(possible_windows):
        before = line[:i]
        block = line[i: i + block_size]
        after = line[i + block_size:]

        if "#" in before:
            break

        if "." in block:
            continue

        if after and after[0] not in ".?":
            continue

        results += check_line(after[1:], nums[1:])
    return results

def q1(filename: str) -> int:
    data = get_data(filename)
    return sum([check_line(line=line, nums=nums) for line, nums in data])

def q2(filename: str) -> int:
    data = get_data(filename)
    return sum([check_line(line="?".join([line] * 5), nums=nums * 5) for line, nums in data])

def test_line():
    assert check_line("???.###", (1, 1, 3)) == 1
    assert check_line(".??..??...?##.", (1, 1, 3)) == 4

def test_q1():
    assert q1("test.txt") == 21
    assert q1("data.txt") == 7379

def test_q2():
    assert q2("test.txt") == 525152
    assert q2("data.txt") == 7732028747925
