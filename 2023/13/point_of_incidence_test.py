# Point of Incidence - https://adventofcode.com/2023/day/13
import pytest

def get_mirrors(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().split("\n\n")

def count_diff_chars(*lines) -> int:
    return sum(len(set(c)) != 1 for c in zip(*lines))

def get_reflection_position(data: list[str], diff: int) -> int:
    for i in range(1, len(data)):
        d1 = reversed(data[:i])
        d2 = data[i:2 * i]

        if sum(count_diff_chars(*lines) for lines in zip(d1, d2)) == diff:
            return i
    return 0

def get_score(mirror: str, diff: int) -> int:
    lines = mirror.splitlines()
    columns = list(zip(*lines))

    return get_reflection_position(columns, diff) + get_reflection_position(lines, diff) * 100

def q1(filename: str, diff) -> int:
    mirrors = get_mirrors(filename)
    return sum(get_score(mirror, diff) for mirror in mirrors)

@pytest.mark.parametrize("filename, result", [("test.txt", 405), ("data.txt", 33122)])
def test_q1(filename: str, result: int):
    assert q1(filename, diff=0) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 400), ("data.txt", 32312)])
def test_q2(filename: str, result: int):
    assert q1(filename, diff=1) == result
