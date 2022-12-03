#!/usr/local/bin/python3

def buildActiveSet(data):
    result = set()

    for y, line in enumerate(data.splitlines()):
        for x, chr in enumerate(line):
            if chr == '#':
                result.add((x, y, 0, 0))

    return result

def getNeigbours(cube):
    for x in range(cube[0]-1, cube[0]+2):
        for y in range(cube[1]-1, cube[1]+2):
            for z in range(cube[2]-1, cube[2] +2):
                for w in range(cube[3]-1, cube[3] +2):
                    if x!=cube[0] or y!=cube[1] or z!=cube[2] or w!=cube[3]:
                        yield (x, y, z, w)

def doCycle(active):
    allInactiveNeighbours = set()
    toBeRemoved = set()
    toBeAdded = set()

    for cube in active:
        neighbours = set(getNeigbours(cube))
        activeNeigbours = neighbours.intersection(active)
        inactiveNeighbours = neighbours.difference(active)

        if not (2 <= len(activeNeigbours) <= 3):
            toBeRemoved.add(cube)

        allInactiveNeighbours.update(inactiveNeighbours)

    for cube in allInactiveNeighbours:
        neighbours = set(getNeigbours(cube))
        activeNeigbours = neighbours.intersection(active)

        if len(activeNeigbours) == 3:
            toBeAdded.add(cube)

    active.difference_update(toBeRemoved)
    active.update(toBeAdded)

def ex1(data, cycles):
    active = buildActiveSet(data)

    for i in range(cycles):
        doCycle(active)

    result = len(active)
    print("Ex1, active elements", result)
    return result


if __name__ == "__main__":
    testData = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert ex1(testData, cycles=1) == 29
    assert ex1(testData, cycles=6) == 848

    assert ex1(data, cycles=6) == 2160