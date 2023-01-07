#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/14

import re
from collections import Counter
from collections import defaultdict

def parsemap(input):
    graph = {}
    pattern = re.compile(r"(\w\w) -> (\w)")
    for line in input:
        match = pattern.match(line)
        graph[match.group(1)] = match.group(2)
    return graph

def ex1(filename, rounds=10):
    data = open(filename, "r").read().splitlines()

    init_string = data[0]
    graph = parsemap(data[2:])
    counter = Counter(init_string)
    pairs = {k: init_string.count(k) for k in graph.keys() if init_string.count(k) > 0}

    for i in range(rounds):
        newpairs = defaultdict(int)
        for (pair, c) in pairs.items():
            l = graph[pair]
            counter[l] += c

            if pair[0] + l in graph:
                newpairs[pair[0] + l] += c
            if l + pair[1] in graph:
                newpairs[l + pair[1]] += c
        pairs = newpairs
    print(counter)
    mc = counter.most_common()
    result = mc[0][1] - mc[-1][1]
    print("EX1 result=", result)
    return result

def test_polymerization_ex1_test():
    assert ex1("test.txt") == 1588

def test_polymerization_ex1_data():
    assert ex1("data.txt") == 2194

def test_polymerization_ex2_test():
    assert ex1("test.txt", rounds=40) == 2188189693529

def test_polymerization_ex2_data():
    assert ex1("data.txt", rounds=40) == 2360298895777
