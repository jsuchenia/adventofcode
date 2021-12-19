#!/usr/local/bin/python3

import re
from collections import Counter

def ex1(lines):
    r = re.compile(r"^(.+) \(contains (.+)\)")

    allAlergens = {}
    allIndigriends = Counter()

    for line in lines:
        indigriends = [x.strip() for x in r.match(line).group(1).split(" ")]
        alergens = [x.strip() for x in r.match(line).group(2).split(",")]

        allIndigriends.update(indigriends)

        for alergen in alergens:
            if alergen not in allAlergens:
                allAlergens[alergen] = set(indigriends)
            else:
                allAlergens[alergen].intersection_update(indigriends)

    print(allAlergens)
    while True:
        countAlergens = {alergen:len(indigriends) for alergen, indigriends in allAlergens.items()}
        nonSolved = [alergen for alergen, count in countAlergens.items() if count > 1]
        solved = [alergen for alergen, count in countAlergens.items() if count == 1]
        empty = [alergen for alergen, count in countAlergens.items() if count == 0]

        print("Solved", solved)
        print("nonSolved", nonSolved)
        print("Empty", empty)

        for alergen in empty:
            del countAlergens[alergen]

        if len(nonSolved) == 0:
            break

        solvedIndigriends = set(indigriend for alergen in solved for indigriend in allAlergens[alergen])
        for alergen in nonSolved:
            allAlergens[alergen].difference_update(solvedIndigriends)

    print(allAlergens)

    for alergen, indigriends in allAlergens.items():
        indigriend = allAlergens[alergen].copy().pop()
        del allIndigriends[indigriend]

    allergens = sorted(allAlergens.keys())
    indigriends = [allAlergens[allergen].pop() for allergen in allergens]
    sortedIndigriends = ','.join(indigriends)
    print("Sorted indigriends", sortedIndigriends)

    result = sum(allIndigriends.values())
    print("Secure indigriends", result)
    return (result, sortedIndigriends)
if __name__ == "__main__":
    test = open("test.txt", "r").read().splitlines()
    data = open("data.txt", "r").read().splitlines()

    assert ex1(test) == (5, "mxmxvkd,sqjhc,fvjkl")
    assert ex1(data) == (2170, "nfnfk,nbgklf,clvr,fttbhdr,qjxxpr,hdsm,sjhds,xchzh")