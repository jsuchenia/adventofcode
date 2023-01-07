#!/usr/local/bin/python3

def calculateGenerations(filename, generations):
    data = [int(x) for x in open(filename, "r").read().strip().split(",")]
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

def test_generations_80_example():
    assert calculateGenerations("example.txt", 10) == 12
    assert calculateGenerations("example.txt", 18) == 26
    assert calculateGenerations("example.txt", 80) == 5934

def test_generations_80_data():
    assert calculateGenerations("data.txt", 80) == 389726

def test_generations_256_example():
    assert calculateGenerations("example.txt", 256) == 26984457539

def test_generations_256_data():
    assert calculateGenerations("data.txt", 256) == 1743335992042
