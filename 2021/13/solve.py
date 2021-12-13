#!/usr/local/bin/python3
from itertools import groupby

def dump(points):
    for y, row in groupby(sorted(points, key=lambda x: x[1]), lambda x:x[1]):
        allX = [point[0] for point in row]
        print(''.join(['#' if i in allX else '.' for i in range(0,max(allX)+1)]))

def executeCommand(points, command):
    val = int(command[13:])
    pos = 1 if command[11] == 'y' else 0

    for point in points:
        if point[pos] > val:
            diff = 2 * (point[pos] - val)
            yield (point[0] - (diff if pos == 0 else 0), point[1] - (diff if pos == 1 else 0))
        elif point[pos] < val:
            yield point

def parse(data):
    (dataLines, commandLines) = data.split("\n\n")
    commands = commandLines.splitlines()
    points = set([tuple([int(s) for s in line.split(",")]) for line in dataLines.splitlines()])
    return points,commands

def doTask(data, runAll=False):
    points, commands = parse(data)

    for cmd in commands:
        points = set(executeCommand(points, cmd))
        if not runAll: break

    result = len(points)
    print("EX{}> Finally we have {} points".format("2" if runAll else "1", result))
    print("Result", points)

    if runAll: dump(points)
    return result

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    input = open("data.txt", "r").read()

    assert doTask(test) == 17
    assert doTask(input) == 827

    assert doTask(test, True) == 16
    assert doTask(input, True) == 104
