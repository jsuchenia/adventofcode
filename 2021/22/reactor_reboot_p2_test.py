#!/usr/local/bin/python3
import re

class Cuboid:
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

        self.difference = []

    def isValid(self):
        return self.xmin <= self.xmax and self.ymin <= self.ymax and self.zmin <= self.zmax

    def subtrack(self, other):
        diff = Cuboid(max(self.xmin, other.xmin), min(self.xmax, other.xmax),
                      max(self.ymin, other.ymin), min(self.ymax, other.ymax),
                      max(self.zmin, other.zmin), min(self.zmax, other.zmax))

        if diff.isValid():
            for s in self.difference:
                s.subtrack(other)

            self.difference.append(diff)

    def getCubic(self):
        myCubics = (self.xmax - self.xmin + 1) * (self.ymax - self.ymin + 1) * (self.zmax - self.zmin + 1)
        otherCubics = sum([s.getCubic() for s in self.difference])

        return myCubics - otherCubics

def parse(data):
    pattern = r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    res = re.compile(pattern)
    for line in data.splitlines():
        m = res.match(line)
        status = True if m.group(1) == "on" else False

        yield (status, int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)), int(m.group(7)))

def p2(filename):
    data = open(filename, "r").read()
    rules = parse(data)

    previousActive = []

    for status, xmin, xmax, ymin, ymax, zmin, zmax in rules:
        cuboid = Cuboid(xmin, xmax, ymin, ymax, zmin, zmax)

        if cuboid.isValid():
            for prev in previousActive:
                prev.subtrack(cuboid)

            if status:
                previousActive.append(cuboid)

    print("Done, now calc!")
    result = sum([act.getCubic() for act in previousActive])
    print("Results are", result)
    return result

def test_calc_reactor_small():
    assert p2("small.txt") == 39

def test_calc_reactor_test():
    assert p2("test.txt") == 39769202357779

def test_calc_reactor_data():
    assert p2("data.txt") == 1325473814582641

def test_calc_reactor_full():
    assert p2("full.txt") == 2758514936282235
