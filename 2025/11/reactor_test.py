# Reactor - https://adventofcode.com/2025/day/11
from functools import cache
from typing import Generator


def get_data(filename: str) -> Generator[tuple[str, list[str]], None, None]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    for line in lines:
        node, elements = line.split(":")
        elements = elements.strip().split(" ")
        yield node, elements


def q1(filename: str) -> int:
    g = {node: elements for node, elements in get_data(filename)}

    @cache
    def scan(node: str, dst: str) -> int:
        if node == dst: return 1
        return sum(scan(n, dst) for n in g.get(node, []))

    return scan("you", "out")


def q2(filename: str) -> int:
    g = {node: elements for node, elements in get_data(filename)}

    @cache
    def scan(node: str, dst: str) -> int:
        if node == dst: return 1
        return sum(scan(n, dst) for n in g.get(node, []))

    total = scan("svr", "fft") * scan("fft", "dac") * scan("dac", "out")
    total += scan("svr", "dac") * scan("dac", "fft") * scan("fft", "out")

    return total


def test_q1():
    assert q1("test.txt") == 5
    assert q1("data.txt") == 615


def test_q2():
    assert q2("test2.txt") == 2
    assert q2("data.txt") == 303012373210128
