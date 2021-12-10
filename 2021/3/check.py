#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/3

def generateString(stats, limit = 500, reversed=False):
    out = ""

    for e in stats:
        if (not reversed and e > limit) or (reversed and e < limit):
            out += "1"
        else:
            out += "0"

    return out

def generateStats(data):
    stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for entry in data:
        for i in range(12):
            if entry[i] == "1":
                stats[i] += 1
    return stats

def ex1(data):
    print("EX1> Len: ", len(data))
    print("EX1> Len1: ", len(data[0].strip()))

    stats = generateStats(data)
    print("Stats> ", stats)
    gamma = generateString(stats)
    epsilon = generateString(stats, reversed=True)
    print("Gamma> ", gamma, int(gamma,2))
    print("Epsilon> ", epsilon, int(epsilon,2))

    result = int(gamma,2) * int(epsilon,2)
    print(">>> EX1 <<< result = ", result)
    return result

def ex2(data):
    oxygen = ex2Gamma(data)
    co2 = ex2Gamma(data, reverse=True)

    result = oxygen * co2
    print(">>> EX2 <<< Result: ", result)
    return result

def ex2Gamma(data, reverse = False):
    stats = generateStats(data)
    print("\n\nEX2> ", stats)
    preffix = ""

    for i in range(12):
        l = len(data)
        stats = generateStats(data)

        print("New stats ", stats)
        print("EX2> filtered len =", l)
        limit = l//2
        print("   limit =", limit)
        e = stats[i]
        if (not reverse and e >= (l-e)) or (reverse and e < (l-e)):
            data = [element for element in data if element[i] == "1"]
            preffix += "1"
        else:
            data = [element for element in data if element[i] == "0"]
            preffix += "0"

        print("Preffix: ", preffix)
        if len(data) == 1:
            break
    if len(data) > 1:
        print("Found more than 1", len(data))
        return 0
    else:
        print("Fount element:", data[0].strip(), int(data[0].strip(), 2))
        return int(data[0].strip(), 2)

if __name__ == "__main__":
    data = open("data", "r").readlines()
    assert ex1(data) == 2583164
    assert ex2(data) == 2784375