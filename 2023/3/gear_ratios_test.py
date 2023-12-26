import math
import re
from collections import defaultdict
from itertools import product
from typing import Iterator

import pytest

def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().splitlines()

def get_neighbours(data: list[str], line_id: int, idx_start: int, idx_stop: int, pattern: str) -> Iterator[tuple[int, int]]:
    for x, y in product(range(line_id - 1, line_id + 2), range(idx_start - 1, idx_stop + 1)):
        if x < 0 or x >= len(data) or y < 0 or y >= len(data[x]):
            continue
        if data[x][y] in pattern:
            yield x, y

def q1(filename: str) -> int:
    data = get_data(filename)
    result = 0
    for line_id, line in enumerate(data):
        for m in re.finditer(r"(\d+)", line):
            if set(get_neighbours(data, line_id, m.start(), m.end(), pattern="*@#$+%/&=-")):
                result += int(m.group())
    return result

def q2(filename: str) -> int:
    data = get_data(filename)
    result: dict[tuple[int, int], set[int]] = defaultdict(set)
    for line_id, line in enumerate(data):
        for m in re.finditer(r"(\d+)", line):
            for adj in set(get_neighbours(data, line_id, m.start(), m.end(), pattern="*")):
                result[adj].add(int(m.group()))
    return sum([math.prod(val) for key, val in result.items() if len(val) == 2])

def test_characters():
    c = set()
    for line in get_data("data.txt"):
        c.update(line)
    assert "".join(sorted(c)) == "#$%&*+-./0123456789=@"

@pytest.mark.parametrize("filename, result", [("test.txt", 4361), ("data.txt", 539590)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 467835), ("data.txt", 80703636)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
