# Point of Incidence - https://adventofcode.com/2023/day/13


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().split("\n\n")

def count_different(line1: str, line2: str) -> int:
    return sum(1 if c1 != c2 else 0 for c1, c2 in zip(line1, line2))

def get_reflection(data: list[str], diff: int) -> int:
    for i in range(1, len(data)):
        d1 = reversed(data[:i])
        d2 = data[i:2 * i]

        if sum(count_different(line1, line2) for line1, line2 in zip(d1, d2)) == diff:
            return i
    return 0

def get_score(mirror: str, diff: int) -> int:
    lines = mirror.splitlines()
    columns = list(zip(*lines))

    return get_reflection(columns, diff) + get_reflection(lines, diff) * 100

def q1(filename: str, diff) -> int:
    mirrors = get_data(filename)
    return sum(get_score(mirror, diff) for mirror in mirrors)

def test_q1():
    assert q1("test.txt", diff=0) == 405
    assert q1("data.txt", diff=0) == 33122

def test_q2():
    assert q1("test.txt", diff=1) == 400
    assert q1("data.txt", diff=1) == 32312
