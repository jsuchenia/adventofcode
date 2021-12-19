#!/usr/local/bin/python3
from itertools import product, permutations, combinations
from collections import Counter

def parse(data):
    return [[tuple([int(x) for x in line.split(',')]) for line in scanner.splitlines()[1:]] for scanner in data.split("\n\n")]

def getTransforrmations():
   ORIENTATIONS = list(product([-1, 1], [-1, 1], [-1, 1]))
   POSITIONS = list(permutations(range(3), 3))

   return list(product(POSITIONS, ORIENTATIONS))

def pointTransform(point, transformation):
    pos = transformation[0]
    direction = transformation[1]

    return tuple(point[pos[i]]*direction[i] for i in range(3))

def calcRealPoints(points, position, transformation):
    transPoints = list(pointTransform(p, transformation) for p in points)
    return list(tuple(x[0] + x[1] for x in zip(p, position)) for p in transPoints)

def checkTwoScanners(pointsA, posA, transformA, pointsB):
    transPointA = calcRealPoints(pointsA, posA, transformA)

    for transform in getTransforrmations():
        transPointsB = [pointTransform(point, transform) for point in pointsB]

        c = Counter([tuple(x[0] - x[1] for x in zip(c[0],c[1])) for c in product(transPointA, transPointsB)])
        mc = c.most_common(1)[0]
        if mc[1] >= 12:
            return mc[0], transform
    return None, None

def ex1(data):
    allpoints = parse(data)
    positions = [None] * len(allpoints)
    transformations = [None] * len(allpoints)

    positions[0] = (0, 0, 0)
    transformations[0] = ((0,1,2), (1,1,1))

    while not all(positions):
        knownPositions = [x for x in range(len(allpoints)) if positions[x] is not None]
        unknownPositions = [x for x in range(len(allpoints)) if positions[x] is None]

        for known, unknown in product(knownPositions, unknownPositions):
            if positions[unknown] is not None:
                break
            print("Checking", known, unknown)
            pos, trans = checkTwoScanners(allpoints[known], positions[known], transformations[known], allpoints[unknown])

            if pos is not None and trans is not None:
                print("Found match", known, unknown)
                positions[unknown] = pos
                transformations[unknown] = trans

    print("All done, calculating!")
    beacons = set()
    for j in range(len(allpoints)):
        beacons.update(calcRealPoints(allpoints[j], positions[j], transformations[j]))

    result = len(beacons)
    maxDistance=0
    print("Found becons", result)

    for posA,posB in combinations(positions, 2):
        m = sum(abs(val1-val2) for val1, val2 in zip(posA,posB))
        if m > maxDistance:
            maxDistance = m

    print("Mnahatan distance", maxDistance)
    return result, maxDistance

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert ex1(test) == (79, 3621)
    assert ex1(data) == (396, 11828)