#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/14

import re
from collections import defaultdict
from collections import Counter

def parseMap(input):
    map = {}
    pattern = re.compile("(\w\w) -> (\w)")
    for line in input:
        match = pattern.match(line)
        map[match.group(1)] = match.group(2)

    return map

def ex1(data, rounds=10):
    input = data[0]
    map = parseMap(data[2:])
    counter = Counter(input)
    pairs = {k:input.count(k) for k in map.keys() if input.count(k) > 0}

    for i in range(rounds):
        newpairs = defaultdict(int)
        for (pair, c) in pairs.items():
            l = map[pair]
            counter[l] += c

            if pair[0] + l in map:
                newpairs[pair[0] + l] += c
            if l + pair[1] in map:
                newpairs[l + pair[1]] += c
        pairs = newpairs
    print(counter)
    mc = counter.most_common()
    result = mc[0][1] - mc[-1][1]
    print("EX1 result=", result)
    return result

if __name__ == "__main__":
    test = open("test.txt", "r").read().splitlines()
    data = open("data.txt", "r").read().splitlines()

    assert ex1(test) == 1588
    assert ex1(data) == 2194

    assert ex1(test, rounds=40) == 2188189693529
    assert ex1(data, rounds=40) == 2360298895777