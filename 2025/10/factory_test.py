# Factory - https://adventofcode.com/2025/day/10
import re
from itertools import combinations
from typing import Generator

from z3 import Int, Optimize, sat

from aoclib import ints

LIGHTS = re.compile(r"\[(.+)]")
BUTTONS = re.compile(r"\(([\d,]+)\)")
JOLTAGE = re.compile(r"{(.*)}")


def get_data(filename: str) -> Generator[tuple[int, list[str], tuple[int, ...]], None, None]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    for line in lines:
        lights = LIGHTS.findall(line)[0].replace(".", "0").replace("#", "1")
        buttons = BUTTONS.findall(line)
        joltage = ints(JOLTAGE.findall(line)[0])
        yield int(lights[::-1], 2), buttons, joltage


def q1(filename: str) -> int:
    total = 0
    for lights, buttons, _ in get_data(filename):
        numbers = [sum(1 << int(bits) for bits in button.split(",")) for button in buttons]

        for n in range(len(numbers) + 1):
            for combo in combinations(numbers, n):
                test = 0
                for b in combo:
                    test ^= b

                if test == lights:
                    total += n
                    break
            else:
                continue
            break
    return total


def q2(filename: str) -> int:
    total = 0
    for _, buttons, joltage in get_data(filename):
        o = Optimize()
        hits = [Int(f"x{i}") for i in range(len(buttons))]
        for hit in hits:
            o.add(hit >= 0)
        o.minimize(sum(hits))
        equations = [0] * len(joltage)
        for i, button in enumerate(buttons):
            for elem in [int(x) for x in button.split(",")]:
                equations[elem] += hits[i]

        for i, joltage in enumerate(joltage):
            o.add(equations[i] == joltage)

        if o.check() == sat:
            model = o.model()
            total += sum(model[v].as_long() for v in hits)
    return total


def test_q1():
    assert q1("test.txt") == 7
    assert q1("data.txt") == 491


def test_q2():
    assert q2("test.txt") == 33
    assert q2("data.txt") == 20617
