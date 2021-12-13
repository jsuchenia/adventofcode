#!/usr/local/bin/python3
from collections import defaultdict

def dump(points):
    d = defaultdict(list)

    for point in points:
        d[point[1]].append(point)

    maxY = max(d.keys())

    for y in range(0,maxY+1):
        if y in d:
            row = d[y]
            allX = [point[0] for point in row]
            maxX = max(allX)
            chars = ['#' if i in allX else '.' for i in range(0,maxX+1)]
            print(''.join(chars))
        else:
            print("")
def executeCommand(points, command):
    val = int(command[13:])
    newPoints = set()

    if command.startswith("fold along y="):
        for point in points:
            if point[1] > val:
                diff = 2* (point[1] - val)
                print("For y={} we have newY={}".format(point[1], point[1] - diff))
                newPoints.add((point[0], point[1] - diff))
            elif point[1] == val:
                continue
            else:
                newPoints.add(point)
    elif command.startswith("fold along x="):
        for point in points:
            if point[0] > val:
                diff = 2*(point[0] - val)
                print("For x={} we have newx={}".format(point[0], point[0] - diff))
                newPoints.add((point[0]-diff, point[1]))
            elif point[0] == val:
                continue
            else:
                newPoints.add(point)

    return newPoints

def ex1(data, runAll=False):
    points = set()

    (dataLines, commandLines) = data.split("\n\n")
    commands = commandLines.splitlines()

    for line in dataLines.splitlines():
        strX,strY = line.split(",")
        points.add((int(strX), int(strY)))

    if runAll:
        for cmd in commands:
            points = executeCommand(points, cmd)
    else:
        points = executeCommand(points, commands[0])

    result = len(points)
    print("EX{}> Finally we have {} points".format("2" if runAll else "1", result))
    print("Result", points)

    if runAll:
        dump(points)
    return result

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    input = open("data.txt", "r").read()

    assert ex1(test) == 17
    assert ex1(input) == 827

    assert ex1(test, True) == 16
    assert ex1(input, True) == 104
