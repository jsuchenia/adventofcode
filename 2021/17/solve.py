#!/usr/local/bin/python3
# My data: x=282..314, y=-80..-45

def checkVelocity(initdx, initdy):
    x = y = 0
    dx = initdx
    dy = initdy
    my = 0

    while y >= -80:
        y += dy
        x += dx

        if y > my: my = y
        if dx >0:
            dx -=1
        dy -= 1

        if -80 <= y <= -45 and 282 <= x <= 314:
            return True, my

    return False, 0

if __name__ == "__main__":
    validInits = set()
    totalmaxy = 0

    for dx in range(1, 500):
        for dy in range(-150, 100):
            valid, maxy = checkVelocity(dx, dy)
            if valid:
                print("Velocity valid", dx, dy)
                validInits.add((dx, dy))
                if maxy > totalmaxy: totalmaxy = maxy

    print("Ex1 result =", totalmaxy)
    print("EX2: Valid velocities", validInits)
    print("EX2 result =", len(validInits))

