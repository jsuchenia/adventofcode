#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/11
# Hint: we can use iter.product however now we supports map with different sizes

def isInRange(a, amax):
    result = (a >= 0 and a < amax)
    return result

def doFlash(table, x, y):
    for dy in range(y - 1, y + 2):
        for dx in range(x - 1, x + 2):
            if dx == x and dy == y:
                continue

            if not isInRange(dy, len(table)):
                continue
            if not isInRange(dx, len(table[dy])):
                continue

            table[dy][dx] += 1

            if table[dy][dx] == 10:
                doFlash(table, dx, dy)

def doCycle(table):
    for y in range(len(table)):
        for x in range(len(table[y])):
            table[y][x] += 1

            if table[y][x] == 10:
                doFlash(table, x, y)

    flashes = 0
    for y in range(len(table)):
        for x in range(len(table[y])):
            if table[y][x] > 9:
                flashes += 1
                table[y][x] = 0
    return flashes

def ex2(filename):
    lines = open(filename, "r").read().splitlines()

    table = [[int(chr) for chr in line] for line in lines]
    size = sum([len(row) for row in table])

    for i in range(1, 300):
        if doCycle(table) == size:
            print("Ex2 all flash at", i)
            return i
    return -1

def ex1(filename):
    lines = open(filename, "r").read().splitlines()
    flashes = 0
    table = [[int(chr) for chr in line] for line in lines]
    for i in range(100):
        flashes += doCycle(table)
    print("Ex1 flashes =", flashes)
    return flashes

def test_octopus_ex1_test():
    assert ex1("test.txt") == 1656

def test_octopus_ex1_data():
    assert ex1("data.txt") == 1644

def test_octopus_ex2_test():
    assert ex2("test.txt") == 195

def test_octopus_ex2_data():
    assert ex2("data.txt") == 229
