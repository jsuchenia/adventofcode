#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/3

def generateString(stats, limit, reversed=False):
    out = ""
    print(f"String {limit=}")

    for e in stats:
        if (not reversed and e > limit) or (reversed and e < limit):
            out += "1"
        else:
            out += "0"

    return out

def generateStats(data):
    stats = [0] * len(data[0].strip())

    for entry in data:
        for i in range(len(entry)):
            if entry[i] == "1":
                stats[i] += 1
    return stats

def ex1(filename):
    data = open(filename, "r").readlines()
    limit = len(data) // 2

    print("EX1> Len: ", len(data))
    print("EX1> Len1: ", len(data[0].strip()))

    stats = generateStats(data)
    print("Stats> ", stats)
    gamma = generateString(stats, limit=limit)
    epsilon = generateString(stats, limit=limit, reversed=True)
    print("Gamma> ", gamma, int(gamma, 2))
    print("Epsilon> ", epsilon, int(epsilon, 2))

    result = int(gamma, 2) * int(epsilon, 2)
    print(">>> EX1 <<< result = ", result)
    return result

def ex2(filename):
    data = open(filename, "r").readlines()

    oxygen = ex2Gamma(data)
    co2 = ex2Gamma(data, reverse=True)

    result = oxygen * co2
    print(">>> EX2 <<< Result: ", result)
    return result

def ex2Gamma(data, reverse=False):
    stats = generateStats(data)
    print("\n\nEX2> ", stats)
    prefix = ""

    for i in range(len(stats)):
        l = len(data)
        stats = generateStats(data)

        print("New stats ", stats)
        print("EX2> filtered len =", l)
        limit = l // 2
        print("   limit =", limit)
        e = stats[i]
        if (not reverse and e >= (l - e)) or (reverse and e < (l - e)):
            data = [element for element in data if element[i] == "1"]
            prefix += "1"
        else:
            data = [element for element in data if element[i] == "0"]
            prefix += "0"

        print("Preffix: ", prefix)
        if len(data) == 1:
            break
    print("Fount element:", data[0].strip(), int(data[0].strip(), 2))
    return int(data[0].strip(), 2)

def test_binary_ex1_example():
    assert ex1("example.txt") == 198

def test_binary_ex1_data():
    assert ex1("data.txt") == 2583164

def test_binary_ex2_example():
    assert ex2("example.txt") == 230

def test_binary_ex2_data():
    assert ex2("data.txt") == 2784375
