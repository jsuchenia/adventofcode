import re
from math import prod

import pytest

def get_data_q1(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    times = [int(n) for n in re.findall(r"(\d+)", lines[0])]
    distances = [int(n) for n in re.findall(r"(\d+)", lines[1])]

    return times, distances

def get_data_q2(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    t = int(re.search(r"(\d+)", lines[0].replace(" ", ""))[1])
    distance = int(re.search(r"(\d+)", lines[1].replace(" ", ""))[1])

    return t, distance

def q1(filename) -> int:
    times, distances = get_data_q1(filename)

    result = [[x * (t - x) > distance for x in range(t)].count(True) for t, distance in zip(times, distances)]
    return prod(result)

def q2(filename) -> int:
    t, distance = get_data_q2(filename)

    return [x * (t - x) > distance for x in range(t)].count(True)

@pytest.mark.parametrize("filename, result", [("test.txt", 288), ("data.txt", 503424)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.skip("Require too many resources")
@pytest.mark.parametrize("filename, result", [("test.txt", 71503), ("data.txt", 32607562)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
