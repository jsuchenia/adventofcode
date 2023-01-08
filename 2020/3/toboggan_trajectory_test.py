#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/3

def checkSlopes(lines, right, down):
    position = 0
    treeCounter = 0
    lineIndex = 0
    size = len(lines[0])

    while lineIndex < len(lines):
        line = lines[lineIndex].strip()
        if line[position] == '#':
            treeCounter += 1

        position = (position + right) % size
        lineIndex += down

    print("Right = ", right, ", down = ", down, ", total trees = ", treeCounter)
    return treeCounter

def part1(filename):
    lines = open(filename).read().splitlines()
    result = checkSlopes(lines, 3, 1)
    print(f"{result=}")

    return result

def part2(filename):
    lines = open(filename).read().splitlines()

    result = checkSlopes(lines, 1, 1)
    result *= checkSlopes(lines, 3, 1)
    result *= checkSlopes(lines, 5, 1)
    result *= checkSlopes(lines, 7, 1)
    result *= checkSlopes(lines, 1, 2)

    print(f"{result=}")
    return result

def test_part1_example():
    assert part1("example.txt") == 7

def test_part1_data():
    assert part1("data.txt") == 184

def test_part2_example():
    assert part2("example.txt") == 336

def test_part2_data():
    assert part2("data.txt") == 2431272960
