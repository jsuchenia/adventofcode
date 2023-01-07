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

def getCubicCosts(data):
    elements = [int(x) for x in data.strip().split(",")]

    m = mean(elements)

    print("mean is ", m)
    mround = int(round(m))
    print("Rounded mean is ", mround)

    result = calculateCubicCosts(elements, mround)
    print("Ex2 Result is ", result)
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

def test_linear_example():
    data = "16,1,2,0,4,2,7,1,2,14"
    assert getLinearCosts(data) == 37

def test_linear_data():
    data = open("data.txt", "r").readline().strip()
    assert getLinearCosts(data) == 352254

def test_cubic_example():
    data = "16,1,2,0,4,2,7,1,2,14"
    assert getCubicCosts(data) == 168

def test_cubic_data():
    data = open("data.txt", "r").readline().strip()
    assert getCubicCosts(data) == 99053183
