#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/12
POSITIONS = "ESWN"

ROTATIONS_R = {90: lambda x, y: (y, -1 * x), 180: lambda x, y: (-1 * x, -1 * y), 270: lambda x, y: (-1 * y, x)}

def ex2(lines):
    x = 10
    y = 1
    xs = ys = 0

    for line in lines:
        code = line[0]
        value = int(line[1:])

        if code == 'F':
          xs += (value * x)
          ys += (value * y)
        elif code == 'N':
            y += value
        elif code == 'S':
            y -= value
        elif code == 'E':
            x += value
        elif code == 'W':
            x -= value
        elif code == 'R':
            (x, y) = ROTATIONS_R[value](x, y)
        elif code == 'L':
            (x, y) = ROTATIONS_R[360-value](x, y)

    print("Ex2 waypoint position x={} y={}".format(x, y))
    print("Ex2 ship position x={} y={}".format(xs, ys))
    result = abs(xs) + abs(ys)
    print("Ex2 result =", result)
    return result

def ex1(lines):
    x = y = 0
    position = 0

    for line in lines:
        code = line[0]
        value = int(line[1:])

        if code == 'F':
            code = POSITIONS[position]

        if code == 'N':
            y += value
        elif code == 'S':
            y -= value
        elif code == 'E':
            x += value
        elif code == 'W':
            x -= value
        elif code == 'R':
            position  = (position + value//90) % len(POSITIONS)
        elif code == 'L':
            change = value//90
            position -= change
            if position < 0:
                position += len(POSITIONS)
            position = position % len(POSITIONS)

    print("Ex1 final position x={} y={}".format(x, y))
    result = abs(x) + abs(y)
    print("Ex1 result =", result)
    return result

if __name__ == "__main__":
    tinput = open("test.txt", "r").read().splitlines()
    input = open("data.txt", "r").read().splitlines()

    assert ex1(tinput) == 25
    assert ex1(input) == 757

    assert ex2(tinput) == 286
    assert ex2(input) == 51249
