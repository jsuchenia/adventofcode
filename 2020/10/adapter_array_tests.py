#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/10

def countDifferences(data):
    plugs = sorted(data)
    plugs.append(plugs[-1] + 3)  # Device is +3 from highest

    diffs = [v if i == 0 else v - plugs[i - 1] for (i, v) in enumerate(plugs)]

    diff1 = len([x for x in diffs if x == 1])
    diff3 = len([x for x in diffs if x == 3])
    result = diff1 * diff3
    print("EX1 result =", result)
    return result

def ex2PermutationCounter(data):
    plugs = sorted(data)
    plugs.append(plugs[-1] + 3)  # Device is +3 from highest

    count = {0: 1}

    for plug in plugs:
        count[plug] = sum([count.get(plug - i, 0) for i in range(1, 4)])

    result = count[plugs[-1]]
    print("Paths =", result)
    return result

def test_difference_test1():
    testInput = [int(x) for x in open("test.txt", "r").readlines()]
    assert countDifferences(testInput) == 35

def test_difference_test2():
    test2Input = [int(x) for x in open("test2.txt", "r").readlines()]
    assert countDifferences(test2Input) == 220

def test_difference_data():
    input = [int(x) for x in open("data.txt", "r").readlines()]
    assert countDifferences(input) == 2244

def test_permutation_test1():
    testInput = [int(x) for x in open("test.txt", "r").readlines()]
    assert ex2PermutationCounter(testInput) == 8

def test_permutation_test2():
    test2Input = [int(x) for x in open("test2.txt", "r").readlines()]
    assert ex2PermutationCounter(test2Input) == 19208

def test_permutation_data():
    input = [int(x) for x in open("data.txt", "r").readlines()]
    assert ex2PermutationCounter(input) == 3947645370368
