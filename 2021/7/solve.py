#!/usr/local/bin/python3
from statistics import median, harmonic_mean, mean


def calculateCubicCosts(data, value):
    total = 0
    for entry in data:
        diff = abs(entry - value)
        e = list(range(1, diff + 1))
        total += sum(e)

    return total


def calculateCosts(data, value):
    sum = 0
    for entry in data:
        sum += abs(entry - value)

    return sum


def getCubicCosts(data, tryDiff=False):
    elements = [int(x) for x in data.strip().split(",")]

    m = mean(elements)

    print("mean is ", m)
    mround = int(round(m))
    print("Rounded mean is ", mround)

    result = calculateCubicCosts(elements, mround)
    print("Ex2 Result is ", result)

    if tryDiff:
        print("For m - 1", m - 1, calculateCubicCosts(elements, mround - 1))
        print("For m + 1", m + 1, calculateCubicCosts(elements, mround + 1))
    return result


def getLinearCosts(data):
    elements = [int(x) for x in data.strip().split(",")]

    print("Median", median(elements))
    print("harmonic_mean", harmonic_mean(elements))
    print("mean", mean(elements))

    m = median(elements)
    result = calculateCosts(elements, m)

    print("Median is ", m)
    print("Ex1 Result is ", result)
    return result


if __name__ == "__main__":
    TEST_DATA = "16,1,2,0,4,2,7,1,2,14"
    data = open("data.txt", "r").readline().strip()

    assert getLinearCosts(TEST_DATA) == 37
    assert getLinearCosts(data) == 352254

    assert getCubicCosts(TEST_DATA) == 168
    getCubicCosts(data, True)
