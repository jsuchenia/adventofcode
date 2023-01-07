#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/18

import math
from itertools import permutations

def doPopulate(pair, left, right):
    if left >= 0 and type(pair[0]) is int:
        pair[0] += left
        return True
    elif left >= 0 and type(pair[0]) is list:
        return doPopulate(pair[0], left, right)
    elif right >= 0 and type(pair[1]) is int:
        pair[1] += right
        return True
    elif right >= 0 and type(pair[1]) is list:
        return doPopulate(pair[1], left, right)

    return False

def doExplode(pair, deep):
    left = pair[0]
    right = pair[1]

    if type(left) is list:
        res, leftres, rightres = doExplode(left, deep + 1)
        if res:
            if rightres >= 0 and leftres >= 0:
                pair[0] = 0

            if rightres >= 0 and type(right) is int:
                pair[1] += rightres
                rightres = -1
            elif rightres >= 0 and type(right) is list:
                doPopulate(pair[1], rightres, -1)
                rightres = -1
            return True, leftres, rightres

    if type(right) is list:
        res, leftres, rightres = doExplode(right, deep + 1)
        if res:
            if rightres >= 0 and leftres >= 0:
                pair[1] = 0

            if leftres >= 0 and type(left) is int:
                pair[0] += leftres
                leftres = -1
            elif leftres >= 0 and type(left) is list:
                doPopulate(pair[0], -1, leftres)
                leftres = -1
            return True, leftres, rightres

    if type(left) is int and type(right) is int and deep > 3:
        print("Explode pair", pair)
        return True, left, right
    return False, -1, -1

def doSplit(pair):
    for i in [0, 1]:
        if type(pair[i]) is int:
            if pair[i] > 9:
                val = pair[i]
                pair[i] = [math.floor(val / 2), math.ceil(val / 2)]
                return True
        elif type(pair[i]) is list:
            if doSplit(pair[i]):
                return True
    return False

def doReduce(pairs):
    while True:
        res, _, _ = doExplode(pairs, 0)
        if res:
            continue
        if doSplit(pairs):
            continue
        break
    return pairs

def doSum(pair1, pair2):
    pairs = [pair1, pair2]
    return doReduce(pairs)

def doSumLines(lines):
    left = eval(lines[0])

    for i in range(1, len(lines)):
        left = doSum(left, eval(lines[i]))

    print("Sum result", left)
    return left

def calcMagniture(pair):
    if type(pair[0]) is int:
        left = pair[0]
    else:
        left = calcMagniture(pair[0])

    if type(pair[1]) is int:
        right = pair[1]
    else:
        right = calcMagniture(pair[1])

    result = 3 * left + 2 * right
    print("Magnitude of {} = {}".format(pair, result))
    return result

def doPermutations(lines):
    m = 0

    for a, b in permutations(list(range(len(lines))), 2):
        res = doSum(eval(lines[a]), eval(lines[b]))
        val = calcMagniture(res)

        if val > m:
            print("new max found", val)
            m = val
    print("Permutations max is", m)
    return m

def test_examples_from_description_reduce():
    # Test examples from a description
    assert doReduce([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
    assert doReduce([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
    assert doReduce([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
    assert doReduce([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    assert doReduce([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

def test_examples_from_description_sum():
    assert doSum([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]) == [
        [[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]

def test_examples_from_description_magnitude():
    assert calcMagniture([9, 1]) == 29
    assert calcMagniture([1, 9]) == 21
    assert calcMagniture([[1, 2], [[3, 4], 5]]) == 143
    assert calcMagniture([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
    assert calcMagniture([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
    assert calcMagniture([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
    assert calcMagniture([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
    assert calcMagniture([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == 3488

def test_e2e_test():
    test = open("test.txt").read().splitlines()

    assert doSumLines(test) == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
    assert calcMagniture([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]) == 4140
    assert doPermutations(test) == 3993

def test_e2e_data():
    data = open("data.txt").read().splitlines()
    assert doSumLines(data) == [[[[6, 8], [9, 7]], [[9, 5], [9, 0]]], [[[9, 9], [5, 7]], [[5, 0], [8, 0]]]]
    assert calcMagniture([[[[6, 8], [9, 7]], [[9, 5], [9, 0]]], [[[9, 9], [5, 7]], [[5, 0], [8, 0]]]]) == 4176

    # Part 2 - find max permutation
    assert doPermutations(data) == 4633
