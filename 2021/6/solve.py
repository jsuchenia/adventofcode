#!/usr/local/bin/python3

def calculateGenerations(data, generations):
    familyMap = {}

    for age in range(9):
        familyMap[age] = data.count(age)

    for gen in range(generations):
        zeroElements = familyMap[0]

        familyMap[0] = familyMap[1]
        familyMap[1] = familyMap[2]
        familyMap[2] = familyMap[3]
        familyMap[3] = familyMap[4]
        familyMap[4] = familyMap[5]
        familyMap[5] = familyMap[6]
        familyMap[6] = familyMap[7] + zeroElements
        familyMap[7] = familyMap[8]
        familyMap[8] = zeroElements

    print("Family after age =", generations, "is ", familyMap, " with total ", to)
    total = sum(familyMap.values())
    print("Total entries ", total)
    return total

if __name__ == "__main__":
    genStr = open("data", "r").readline()
    data = [int(x) for x in genStr.split(",")]

    assert calculateGenerations([3,4,3,1,2], 10) == 12
    assert calculateGenerations([3,4,3,1,2], 18) == 26
    assert calculateGenerations([3,4,3,1,2], 80) == 5934
    assert calculateGenerations(data, 80) == 389726

    assert calculateGenerations(data, 256) == 1743335992042
