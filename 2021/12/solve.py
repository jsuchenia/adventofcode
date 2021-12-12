#!/usr/local/bin/python3
from collections import defaultdict

def parse(lines):
    map = defaultdict(list)

    for line in lines:
        (src, dst)=line.split("-")
        map[src].append(dst)
        map[dst].append(src)
    return map

def canIVisit(visitedList, next, maxSmallVisits):
    tmp = list(visitedList)
    tmp.append(next)

    tmp = [node for node in tmp if node.islower()]

    doubleVisits = 0

    for key in set(tmp):
        c = tmp.count(key)
        if c > 2:
            return False
        elif c == 2:
            doubleVisits += 1
            if doubleVisits > maxSmallVisits:
                return False
    return True


def doVisit(map, visitedList, entry, maxSmallVisits=0):
    visitedCounter = 0

    tmp = list(visitedList)
    tmp.append(entry)

    if entry == "end":
        print("Visited path", tmp)
        return 1

    for next in map[entry]:
        if next == "start":
            continue
        if next.islower() and not canIVisit(tmp, next, maxSmallVisits):
            # print("  -> Entry {} already visited, and it's small - {}".format(next, tmp))
            continue

        # print("Checking connection {} -> {}".format(entry, next))
        visitedCounter += doVisit(map, tmp, next, maxSmallVisits)

    return visitedCounter

def ex1(lines):
    map = parse(lines)
    print("Prepared MAP:", map)
    result = doVisit(map, [], "start")
    print("Ex1 result", result)
    return result

def ex2(lines):
    map = parse(lines)
    print("Prepared MAP:", map)
    result = doVisit(map, [], "start", maxSmallVisits=1)
    print("Ex1 result", result)
    return result

if __name__ == "__main__":
    test1 = open("test1.txt", "r").read().splitlines()
    test2 = open("test2.txt", "r").read().splitlines()
    test3 = open("test3.txt", "r").read().splitlines()
    data = open("data.txt", "r").read().splitlines()

    assert ex1(test1) == 10
    assert ex1(test2) == 19
    assert ex1(test3) == 226
    assert ex1(data) == 3495

    assert ex2(test1) == 36
    assert ex2(test2) == 103
    assert ex2(test3) == 3509
    assert ex2(data) == 94849
