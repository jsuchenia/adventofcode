# Never Tell Me The Odds - https://adventofcode.com/2023/day/24
from dataclasses import dataclass
from itertools import combinations

import pytest
from sympy import Symbol, Eq, solve, symbols

@dataclass(frozen=True)
class Hailstone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

def get_data(filename: str) -> list[Hailstone]:
    with open(filename) as f:
        return [Hailstone(*map(int, line.split(','))) for line in f.read().strip().replace('@', ',').splitlines()]

def q1(filename: str, min_val: int, max_val: int) -> int:
    hs = get_data(filename)

    c = 0
    for a, b in combinations(hs, 2):
        # Sympy
        ta, tb = Symbol("ta"), Symbol("tb")

        eq_x = Eq(a.dx * ta + a.x, b.dx * tb + b.x)
        eq_y = Eq(a.dy * ta + a.y, b.dy * tb + b.y)

        result = solve([eq_x, eq_y], ta, tb)
        if result and result[ta] > 0 and result[tb] > 0:
            pos_x = a.dx * result[ta] + a.x
            pos_y = a.dy * result[ta] + a.y
            if min_val <= pos_x <= max_val and min_val <= pos_y <= max_val:
                c += 1
    return c

def q2(filename: str) -> int:
    hs = get_data(filename)
    x, y, z, dx, dy, dz = sym = symbols('x y z dx dy dz')

    equations = []
    variables = [*sym]
    for idx, a in enumerate(hs[:3]):
        t = Symbol(f't_{idx}')  # remember that each intersection will have a different time, so it needs its own variable

        equations.append(Eq(x + dx * t, a.dx * t + a.x))
        equations.append(Eq(y + dy * t, a.dy * t + a.y))
        equations.append(Eq(z + dz * t, a.dz * t + a.z))
        variables.append(t)

    result = solve(equations, *variables)
    return sum(result[0][:3])

@pytest.mark.skip
def test_q1():
    assert q1("test.txt", min_val=7, max_val=27) == 2
    assert q1("data.txt", min_val=200000000000000, max_val=400000000000000) == 16727

def test_q2():
    assert q2("test.txt") == 47
    assert q2("data.txt") == 606772018765659
