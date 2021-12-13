#!/usr/local/bin/python3
from itertools import groupby

def dump(points):
    for y, row in groupby(sorted(points, key=lambda x: x[1]), lambda x:x[1]):
        allX = [point[0] for point in row]
        print(''.join(['#' if i in allX else ' ' for i in range(0,max(allX)+1)]))

def parse(data):
    (dataLines, commandLines) = data.split("\n\n")
    commands = commandLines.splitlines()
    points = set(tuple(map(int, line.split(","))) for line in dataLines.splitlines())
    return points,commands

def doTask(data, runAll=False):
    points, commands = parse(data)

    for cmd in commands:
        foldValue = int(cmd[13:])
        axis = 1 if cmd[11] == 'y' else 0
        points = {tuple(min(2*foldValue - val, val) if i==axis else val for i, val in enumerate(point)) for point in points}
        if not runAll: break

    result = len(points)
    print("EX{}> Finally we have {} points".format("2" if runAll else "1", result))
    print("Result", result)

    if runAll: dump(points)
    return result

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    input = open("data.txt", "r").read()

    assert doTask(test) == 17
    assert doTask(input) == 827

    assert doTask(test, runAll=True) == 16
    assert doTask(input, runAll=True) == 104
