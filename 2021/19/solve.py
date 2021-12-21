#!/usr/local/bin/python3
from itertools import product, permutations, combinations
from collections import Counter

#Parse input
def parse(data):
    return [[tuple([int(x) for x in line.split(',')]) for line in scanner.splitlines()[1:]] for scanner in data.split("\n\n")]

# Generator for all posibble transformations
def getTransforrmations():
   ORIENTATIONS = product([-1, 1], [-1, 1], [-1, 1])
   POSITIONS = permutations(range(3), 3)

   return product(POSITIONS, ORIENTATIONS)

# transform one point according to definiton
def pointTransform(point, transformation):
    pos = transformation[0]
    direction = transformation[1]

    return tuple(point[pos[i]]*direction[i] for i in range(3))

# Transform points to a common view
def calcRealPoints(points, scanner):
    scannerTransformation = scanner[1]
    scannerPosition = scanner[0]
    transPoints = [pointTransform(p, scannerTransformation) for p in points]
    return [tuple(sum(x) for x in zip(p, scannerPosition)) for p in transPoints]

# Check all transformations to see if at least 12 points will show us scanner position
def findScannerDetails(pointsA, scannerA, pointsB):
    transPointsA = calcRealPoints(pointsA, scannerA)

    # Check which transformation will generate 12 values pointing to new scanner B position
    # This position + verified transformation will help us normalize points
    for trans in getTransforrmations():
        transPointsB = (pointTransform(point, trans) for point in pointsB)

        counts = Counter((tuple(x[0] - x[1] for x in zip(pointA, pointB)) for pointA, pointB in product(transPointsA, transPointsB)))
        mc = counts.most_common(1)[0]
        if mc[1] >= 12:
            return (mc[0], trans)
    return None

# Do a whole task
def doCheck(data):
    scannersPoints = parse(data)
    scannerDetails = [None] * len(scannersPoints)

    # Initial position of scannerA, it will be the mail point view for a whole task
    scannerDetails[0] = ((0, 0, 0), ((0,1,2), (1,1,1)))

    while not all(scannerDetails):
        knownPositions = [x for x in range(len(scannerDetails)) if scannerDetails[x] is not None]
        unknownPositions = [x for x in range(len(scannerDetails)) if scannerDetails[x] is None]

        for known, unknown in product(knownPositions, unknownPositions):
            unknownDetails = findScannerDetails(scannersPoints[known], scannerDetails[known], scannersPoints[unknown])

            if unknownDetails is not None:
                print("Found match", known, unknown)
                scannerDetails[unknown] = unknownDetails
                break

    print("All done, calculating all beacons!")
    beacons = set(point for j in range(len(scannersPoints)) for point in calcRealPoints(scannersPoints[j], scannerDetails[j]))
    result = len(beacons)
    print("Found normalized beacons", result)

    positions = [p[0] for p in scannerDetails]

    maxManhDistance = max(sum(abs(val1-val2) for val1, val2 in zip(posA,posB)) for posA,posB in combinations(positions, 2))
    print("Mnahatan distance", maxManhDistance)
    return result, maxManhDistance

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert doCheck(test) == (79, 3621)
    assert doCheck(data) == (396, 11828)