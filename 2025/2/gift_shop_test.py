# Gift Shop - https://adventofcode.com/2025/day/2
from typing import Iterator


def get_data(filename: str) -> Iterator[tuple[str, str]]:
    with open(filename) as f:
        for range in f.read().strip().split(','):
            start, stop = range.split('-')
            assert int(start) <= int(stop), 'start must be less than stop'
            yield start, stop


def q1(filename: str) -> int:
    total = 0
    for start, stop in get_data(filename):
        if len(start) % 2 == 1:
            start = "0" + start
        pref_start, pref_stop = int(start[:len(start) // 2]), int(stop[:-len(start) // 2])
        start, stop = int(start), int(stop)

        for idx in range(pref_start, pref_stop + 1):
            potential = int(f"{idx}{idx}")
            if start <= potential <= stop:
                # print(f"POTENTIAL: {potential=}")
                total += potential

    return total


def q2(filename: str) -> int:
    total = 0
    for start, stop in get_data(filename):
        for x in range(int(start), int(stop) + 1):
            x_str = str(x)
            for l in range(1, len(x_str) // 2 + 1):
                if x_str[:l] * (len(x_str) // l) == x_str:
                    # print(f"POTENTIAL: {x=}")
                    total += x
                    break

    return total


def test_q1():
    assert q1("test.txt") == 1227775554
    assert q1("data.txt") == 28146997880


def test_q2():
    assert q2("test.txt") == 4174379265
    assert q2("data.txt") == 40028128307
