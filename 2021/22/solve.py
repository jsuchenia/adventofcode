#!/usr/local/bin/python3
import re
from itertools import product

def parse(data):
    pattern = r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    res = re.compile(pattern)
    for line in data.splitlines():
        m = res.match(line)
        status = True if m.group(1) == "on" else False
        x = [int(m.group(2)), int(m.group(3))]
        y = [int(m.group(4)), int(m.group(5))]
        z = [int(m.group(6)), int(m.group(7))]

        yield {"status": status, "x": x, "y":y, "z":z}

def isValid(rule):
    x = rule["x"]
    y = rule["y"]
    z = rule["z"]

    for val in (x, y, z):
        if val[0] > 50 or val[1] < -50:
            return False
    return True

def ex1(data):
    rules = parse(data)

    points = set()

    for rule in rules:
        if isValid(rule):
            x = rule["x"]
            y = rule["y"]
            z = rule["z"]

            status = rule["status"]

            for point in product(range(x[0], x[1]+1), range(y[0], y[1]+1), range(z[0], z[1]+1)):
                if status:
                    points.add(point)
                else:
                     if point in points: points.remove(point)
    result = len(points)
    print("Finally we have", result)
    return result

if __name__ == "__main__":
    small = open("small.txt", "r").read()
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()
    full = open("full.txt", "r").read()

    assert ex1(small) == 39
    assert ex1(test) == 590784
    assert ex1(data) == 581108
    assert ex1(full) == 474140