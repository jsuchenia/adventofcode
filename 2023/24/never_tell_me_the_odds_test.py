# Never Tell Me The Odds - https://adventofcode.com/2023/day/24
from dataclasses import dataclass
from itertools import combinations

from sympy import Symbol, Eq, solve, symbols, lambdify

@dataclass(frozen=True)
class Hailstone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    def get_xy(self):
        return self.x, self.y, self.dx, self.dy

def get_data(filename: str) -> list[Hailstone]:
    with open(filename) as f:
        return [Hailstone(*map(int, line.split(','))) for line in f.read().strip().replace('@', ',').splitlines()]

def prepare_functions():
    ta, tb = symbols("ta tb")
    adx, ax, ady, ay = symbols("adx ax ady ay")
    bdx, bx, bdy, by = symbols("bdx bx bdy by")

    results = solve([Eq(adx * ta + ax, bdx * tb + bx), Eq(ady * ta + ay, bdy * tb + by)], ta, tb)

    fun_ta = lambdify(((ax, ay, adx, ady), (bx, by, bdx, bdy)), results[ta])
    fun_tb = lambdify(((ax, ay, adx, ady), (bx, by, bdx, bdy)), results[tb])

    return fun_ta, fun_tb

def q1_sympy(filename: str, min_val: int, max_val: int) -> int:
    hs = get_data(filename)

    fun_ta, fun_tb = prepare_functions()

    c = 0
    for a, b in combinations(hs, 2):
        try:
            ta = fun_ta(a.get_xy(), b.get_xy())
            tb = fun_tb(a.get_xy(), b.get_xy())
        except ZeroDivisionError:
            continue

        if ta <= 0 or tb <= 0:
            continue

        x, y = a.dx * ta + a.x, a.dy * ta + a.y

        if min_val <= x <= max_val and min_val <= y <= max_val:
            c += 1
    return c

def q1_math(filename: str, min_val: int, max_val: int) -> int:
    """ Based on https://stackoverflow.com/a/38977789/3190453 """

    hs = get_data(filename)

    c = 0
    for a, b in combinations(hs, 2):
        x1, y1 = a.x, a.y  # Position now
        x2, y2 = a.x + a.dx, a.y + a.dy  # After one step

        x3, y3 = b.x, b.y
        x4, y4 = b.x + b.dx, b.y + b.dy

        if (denominator := ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))) == 0:
            continue

        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        px, py = x1 + ua * (x2 - x1), y1 + ua * (y2 - y1)

        if not min_val <= px <= max_val or not min_val <= py <= max_val:
            continue

        # px grow when x2 grow - checking if it happened in a future, both true or both false
        if (px > x1) == (x2 > x1) and (px > x3) == (x4 > x3):
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

def test_q1_sympy():
    assert q1_sympy("test.txt", min_val=7, max_val=27) == 2
    assert q1_sympy("data.txt", min_val=200000000000000, max_val=400000000000000) == 16727

def test_q1_math():
    assert q1_math("test.txt", min_val=7, max_val=27) == 2
    assert q1_math("data.txt", min_val=200000000000000, max_val=400000000000000) == 16727

def test_q2():
    assert q2("test.txt") == 47
    assert q2("data.txt") == 606772018765659
