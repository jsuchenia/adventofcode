# Lobby - https://adventofcode.com/2025/day/3


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    return lines


def find_max_number(bank: str, size: int) -> int:
    numbers = list(map(int, bank))
    result = 0
    last_idx = 0
    for i in range(size):
        remaining_idx = size - i - 1
        next_max = max(numbers[last_idx:len(numbers) - remaining_idx])
        next_max_idx = numbers.index(next_max, last_idx)

        result = 10 * result + next_max
        last_idx = next_max_idx + 1
    return result


def q1(filename: str) -> int:
    return sum([find_max_number(bank, 2) for bank in get_data(filename)])


def q2(filename: str) -> int:
    return sum([find_max_number(bank, 12) for bank in get_data(filename)])


def test_q1():
    assert q1("test.txt") == 357
    assert q1("data.txt") == 17346


def test_q2():
    assert q2("test.txt") == 3121910778619
    assert q2("data.txt") == 172981362045136
