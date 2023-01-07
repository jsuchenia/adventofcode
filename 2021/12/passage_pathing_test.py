#!/usr/local/bin/python3
from collections import defaultdict

def parse(lines):
    data = defaultdict(list)

    for line in lines:
        (src, dst) = line.split("-")
        data[src].append(dst)
        data[dst].append(src)
    return data

def canIVisit(visitedList, next, maxSmallVisits):
    tmp = list(visitedList)
    tmp.append(next)

    tmp = [node for node in tmp if node.islower()]

    double_visits = 0

    for key in set(tmp):
        c = tmp.count(key)
        if c > 2:
            return False
        elif c == 2:
            double_visits += 1
            if double_visits > maxSmallVisits:
                return False
    return True

def doVisit(map, visitedList, entry, maxSmallVisits=0):
    visited_counter = 0

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
        visited_counter += doVisit(map, tmp, next, maxSmallVisits)

    return visited_counter

def ex1(filename):
    lines = open(filename, "r").read().splitlines()
    graph = parse(lines)
    print("Prepared MAP:", graph)
    result = doVisit(graph, [], "start")
    print("Ex1 result", result)
    return result

def ex2(filename):
    lines = open(filename, "r").read().splitlines()
    graph = parse(lines)
    print("Prepared MAP:", graph)
    result = doVisit(graph, [], "start", maxSmallVisits=1)
    print("Ex1 result", result)
    return result

def test_passage_ex1_test1():
    assert ex1("test1.txt") == 10

def test_passage_ex1_test2():
    assert ex1("test2.txt") == 19

def test_passage_ex1_test3():
    assert ex1("test3.txt") == 226

def test_passage_ex1_data():
    assert ex1("data.txt") == 3495

def test_passage_ex2_test1():
    assert ex2("test1.txt") == 36

def test_passage_ex2_test2():
    assert ex2("test2.txt") == 103

def test_passage_ex2_test3():
    assert ex2("test3.txt") == 3509

def test_passage_ex2_data():
    assert ex2("data.txt") == 94849
