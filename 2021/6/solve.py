#!/usr/local/bin/python3

def calculateGenerations(data, generations):
    fishFamily = [0] * 9

    for age in range(9):
        fishFamily[age] = data.count(age)

    for gen in range(generations):
        zeroElements = fishFamily.pop(0)
        fishFamily.append(zeroElements)
        fishFamily[6] += zeroElements

    total = sum(fishFamily)
    print("Family after age =", generations, "is ", fishFamily, " with total ", total)
    return total

if __name__ == "__main__":
    genStr = open("data", "r").readline()
    data = [int(x) for x in genStr.split(",")]

    TEST_DATA = [3, 4, 3, 1, 2]
    assert calculateGenerations(TEST_DATA, 10) == 12
    assert calculateGenerations(TEST_DATA, 18) == 26
    assert calculateGenerations(TEST_DATA, 80) == 5934

    assert calculateGenerations(data, 80) == 389726
    assert calculateGenerations(data, 256) == 1743335992042
