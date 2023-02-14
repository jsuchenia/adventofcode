#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/9

def checkIfValid(n, acc):
    for a in acc:
        if n > a:
            rest = n - a
            if rest != a and rest in acc:
                return True
    return False

def findFirstWrongNumber(data, boxSize):
    numbers = [int(x) for x in data]

    acc = []

    for n in numbers:
        if len(acc) < boxSize:
            acc.append(n)
        else:
            if checkIfValid(n, acc):
                acc.pop(0)
                acc.append(n)
            else:
                return n

    return -1

def findSum(data, n):
    numbers = [int(x) for x in data]
    acc = []

    for a in numbers:
        # Shring list
        while sum(acc) >= n and len(acc) > 0:
            acc.pop(0)

        acc.append(a)

        while sum(acc) > n and len(acc) > 0:
            acc.pop(0)

        if (len(acc) > 1) and (sum(acc) == n):
            return min(acc) + max(acc)
    return -1

def test_first_wrong_number_example():
    data = open("test.txt", "r").readlines()
    assert findFirstWrongNumber(data, 5) == 127

def test_first_wrong_number_data():
    data = open("data.txt", "r").readlines()
    assert findFirstWrongNumber(data, 25) == 257342611

def test_sum_example():
    data = open("test.txt", "r").readlines()
    assert findSum(data, 127) == 62

def test_sum_data():
    data = open("data.txt", "r").readlines()
    assert findSum(data, 257342611) == 35602097
