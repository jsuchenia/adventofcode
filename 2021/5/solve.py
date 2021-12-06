#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/5

def getPoint(pointStr):
        return [ int(x) for x in pointStr.split(",")]

# X is the same
def getVerticalPoints(start, end):
    x = start[0]

    a = min(start[1], end[1])
    b = max(start[1], end[1])

    return ["{},{}".format(x, y) for y in range(a, b+1)]

# Y is the same
def getHorizontalPoints(start, end):
    y = start[1]

    a = min(start[0], end[0])
    b = max(start[0], end[0])

    return ["{},{}".format(x, y) for x in range(a, b+1)]

# Y is the same
def getDiagonalPoints(start, end):
    xa = start[0]
    xb = end[0]

    ya = start[1]
    yb = end[1]

    if abs(xb - xa) != abs(yb - ya):
        print("Not diagonal line", start, "->", end)
        return []

    elements = abs(xb - xa)

    xdelta = 1 if xb > xa else -1
    ydelta = 1 if yb > ya else -1

    rc = ["{},{}".format(xa + e*xdelta, ya + e*ydelta) for e in range(0, elements + 1)]
    return rc

def countDangerPoints(data, withDiagonal = False):
    table = {}
    for line in data:
        index = line.find("->")
        l = line.strip()

        start = getPoint(l[0:index])
        end = getPoint(l[index+2:])

        if start[0] == end[0]:
            points = getVerticalPoints(start,end)
        elif start[1] == end[1]:
            points = getHorizontalPoints(start, end)
        elif withDiagonal:
            points = getDiagonalPoints(start, end)
        else:
            points = []

        for point in points:
            if point in table:
                table[point] += 1
            else:
                table[point] = 1

    print("All points =", len(table))
    dangerPoints = [key for (key, value) in table.items() if value > 1]
    print("Danger points =", len(dangerPoints))

    return len(dangerPoints)


if __name__ == "__main__":
    data = open("data", "r").readlines()

    assert countDangerPoints(data, withDiagonal=False) == 8060
    assert countDangerPoints(data, withDiagonal=True) == 21577
