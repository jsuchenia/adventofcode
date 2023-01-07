#!/usr/local/bin/python3
# My data.txt: x=282..314, y=-80..-45

def check_velocity(initdx, initdy, x1, x2, y1, y2):
    x = y = 0
    dx = initdx
    dy = initdy
    my = 0

    while y >= y1:
        y += dy
        x += dx

        if y > my: my = y
        if dx > 0:
            dx -= 1
        dy -= 1

        if y1 <= y <= y2 and x1 <= x <= x2:
            return True, my

    return False, 0

def solve(x1, x2, y1, y2):
    validInits = set()
    totalmaxy = 0

    for dx in range(1, 500):
        for dy in range(-150, 100):
            valid, maxy = check_velocity(dx, dy, x1, x2, y1, y2)
            if valid:
                print("Velocity valid", dx, dy)
                validInits.add((dx, dy))
                if maxy > totalmaxy: totalmaxy = maxy

    result1 = totalmaxy
    result2 = len(validInits)
    print("Ex1 result =", result1)
    print("EX2: Valid velocities", validInits)
    print("EX2 result =", result2)
    return result1, result2

def test_solve_example():
    assert solve(20, 30, -10, -5) == (45, 112)

def test_solve_data():
    assert solve(282, 314, -80, -45) == (3160, 1928)
