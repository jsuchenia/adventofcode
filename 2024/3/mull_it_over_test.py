# Mull It Over - https://adventofcode.com/2024/day/3
import re


def get_data(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def q1(filename: str) -> int:
    data = get_data(filename)

    return sum(int(a) * int(b) for a, b in re.findall(r'mul\((\d+),(\d+)\)', data))


def q2(filename: str) -> int:
    data = get_data(filename)
    res = 0
    enabled = True

    for part in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data):
        if part.startswith("mul") and enabled:
            a, b = re.findall(r'mul\((\d+),(\d+)\)', part)[0]
            res += int(a) * int(b)
        elif part.startswith("do("):
            enabled = True
        elif part.startswith("don"):
            enabled = False
    return res


def test_q1():
    assert q1("test.txt") == 161
    assert q1("data.txt") == 160672468


def test_q2():
    assert q2("test2.txt") == 48
    assert q2("data.txt") == 84893551
