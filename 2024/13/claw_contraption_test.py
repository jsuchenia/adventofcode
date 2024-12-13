# Claw Contraption - https://adventofcode.com/2024/day/13
import re

from sympy import symbols, Eq, solve


def get_data(filename: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    with open(filename) as f:
        lines = f.read().strip()

    machines = lines.split('\n\n')
    result = []
    for machine in machines:
        lines = machine.splitlines()
        a_x, a_y = re.findall(r'Button A: X\+(\d+), Y\+(\d+)', lines[0])[0]
        b_x, b_y = re.findall(r'Button B: X\+(\d+), Y\+(\d+)', lines[1])[0]
        prize_x, prize_y = re.findall(r'Prize: X=(\d+), Y=(\d+)', lines[2])[0]
        
        result.append(((int(a_x), int(a_y)), (int(b_x), int(b_y)), (int(prize_x), int(prize_y))))
    return result


def q1(filename: str, *, boost=0) -> int:
    tokens = 0
    machines = get_data(filename)
    for machine in machines:
        def_a, def_b, prize = machine
        A, B = symbols("A"), symbols("B")

        result = solve([
            Eq(A * def_a[0] + B * def_b[0], prize[0] + boost),
            Eq(A * def_a[1] + B * def_b[1], prize[1] + boost),
        ], [A, B])

        if result[A].is_integer and result[B].is_integer:
            tokens += 3 * result[A] + result[B]

    return tokens


def test_q1():
    assert q1("test.txt") == 480
    assert q1("data.txt") == 29711


def test_q2():
    assert q1("test.txt", boost=10_000_000_000_000) == 875318608908
    assert q1("data.txt", boost=10_000_000_000_000) == 94955433618919
