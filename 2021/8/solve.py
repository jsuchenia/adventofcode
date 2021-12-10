#!/usr/local/bin/python3
from itertools import groupby

def ssig(sig):
    return ''.join(sorted(sig.strip()))

def ext2GetValue(line):
    (left, right) = line.split(" | ")

    sigs = sorted([ssig(sig) for sig in left.strip().split(" ")], key=lambda x: len(x))
    dictByLen={k:list(v) for (k, v) in groupby(sigs, lambda x: len(x))}

    # Known static mappings
    mapping = {"1": dictByLen[2][0], "4": dictByLen[4][0], "7": dictByLen[3][0], "8": dictByLen[7][0]}

    # 6 is used as a pattern for 5
    mapping["6"] = [x for x in dictByLen[6] if not set(dictByLen[3][0]).issubset(set(x))][0]
    mapping["5"] = [x for x in dictByLen[5] if set(x).issubset(set(mapping["6"]))][0]

    # 3 Is used as a pattern for 9, 0
    mapping["3"] = [x for x in dictByLen[5] if set(dictByLen[3][0]).issubset(set(x))][0]
    mapping["9"] = [x for x in dictByLen[6] if set(mapping["3"]).issubset(set(x))][0]
    mapping["0"] = [x for x in dictByLen[6] if (not set(mapping["3"]).issubset(set(x))) and x != mapping["6"]][0]

    # 2 the rest from len5
    mapping["2"] = [x for x in dictByLen[5] if (x != mapping["5"]) and (x != mapping["3"])][0]

    # Reverse mapping
    mapping = {v:k for (k,v) in mapping.items()}
    return int(''.join([mapping[ssig(sig)] for sig in right.strip().split(" ")]))

def ex2CountAll(data):
    result = sum([ext2GetValue(line) for line in data])
    print("EX2 result", result)
    return result

def ex1FilterAndCount(sigs): # Count how many special items are in one line
    return len([s for s in sigs if len(s) in [2, 3, 4, 7]])

def ex1CountKnown(lines): # Parse input and execute ex1FilterAndCount() for each line
    total = sum([ex1FilterAndCount(l.strip().split(" | ")[1].split(" ")) for l in lines])
    print("EX1 result =", total)
    return total

if __name__ == "__main__":
    testData = open("test.txt", "r").readlines()
    data = open("data.txt", "r").readlines()

    assert ex1CountKnown(testData) == 26
    assert ex1CountKnown(data) == 512
    assert ex2CountAll(testData) == 61229
    assert ex2CountAll(data) == 1091165
