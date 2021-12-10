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
                print("Ex1 > Invalid number ", n)
                return n

    print("Can't find correct number")
    return -1

def findSum(data, n):
    numbers = [int(x) for x in data]
    acc = []

    for a in numbers:
        #Shring list
        while sum(acc) >= n and len(acc) > 0:
            print("List to big, removing element")
            acc.pop(0)

        print("adding new element", a)
        acc.append(a)

        while sum(acc) > n and len(acc) > 0:
            print("List to big, removing element")
            acc.pop(0)

        print("Now sum is", sum(acc), " for list =", acc)

        if (len(acc) > 1) and (sum(acc) == n):
            print("Found a list", acc)
            return min(acc) + max(acc)
        else:
            print("List not valid")
    print("List not found")
    return -1

if __name__ == "__main__":
    data = open("data.txt", "r").readlines()
    testData = open("test.txt", "r").readlines()

    assert findFirstWrongNumber(testData, 5) == 127
    assert findFirstWrongNumber(data, 25) == 257342611

    assert findSum(testData, 127) == 62
    print(findSum(data, 257342611))
