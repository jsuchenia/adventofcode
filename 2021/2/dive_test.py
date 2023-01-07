#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/2

def ex1(filename):
    data = open(filename, "r").readlines()
    position = 0
    depth = 0

    for entry in data:
        if entry.startswith("forward "):
            position += int(entry[8:])
        elif entry.startswith("down "):
            depth += int(entry[5:])
        elif entry.startswith("up "):
            depth -= int(entry[3:])
        else:
            print("Unknown command", entry)

    print("[ex1] Position =", position)
    print("[ex1] Depth =", depth)
    solution = position * depth
    print("[ex1] Solution1 = ", solution)
    return solution

def ex2(filename):
    data = open(filename, "r").readlines()

    aim = 0
    depth = 0
    position = 0

    for entry in data:
        if entry.startswith("forward "):
            position += int(entry[8:])
            depth += (aim * int(entry[8:]))
        elif entry.startswith("down "):
            aim += int(entry[5:])
        elif entry.startswith("up "):
            aim -= int(entry[3:])
        else:
            print("Unknown command", entry)

    print("ex2> Position =", position)
    print("ex2> Depth =", depth)
    solution = position * depth
    print("ex2> Solution = ", solution)
    return solution

def test_dive_ex1_example():
    assert ex1("example.txt") == 150

def test_dive_ex1_data():
    assert ex1("data.txt") == 1893605

def test_dive_ex2_example():
    assert ex2("example.txt") == 900

def test_dive_ex2_data():
    assert ex2("data.txt") == 2120734350
