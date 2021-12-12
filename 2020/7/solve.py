#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/7

from collections import defaultdict

MY_BAG = "shiny gold bag"

def buildReversedGraph(data):
    graph = defaultdict(set)

    for line in data:
        position = line.find("contain")
        what = line[0:position].strip()
        elements = line[position + 8:].strip()

        if elements == "no other bags.":
            continue

        if elements[-1] == '.':
            elements = elements[:-1]

        if what.endswith("bags"):
            what = what[:-1]

        for element in elements.split(","):
            element = element.strip()
            if element[0].isdigit():
                element = element[2:].strip()
            if element.endswith("bags"):
                element = element[:-1].strip()
            graph[element].add(what)
    return graph

def buildBagsGraph(data):
    graph = defaultdict(dict)
    for line in data:
        position = line.find("contain")
        what = line[0:position].strip()
        elements = line[position + 8:].strip()

        if what.endswith("bags"):
            what = what[:-1]

        if elements == "no other bags.":
            graph[what] = {}
            continue

        if elements[-1] == '.':
            elements = elements[:-1]

        for element in elements.split(","):
            element = element.strip()
            counter = int(element[0])
            element = element[2:].strip()

            if element.endswith("bags"):
                element = element[:-1].strip()

            graph[what][element] = counter
    return graph

def ex1CalculateBagColors(data, myBag):
    graph = buildReversedGraph(data)
    foundElements = set(graph[myBag])

    found = True
    while found:
        found = False
        elementsToAdd = set()

        for element in foundElements:
            outerBags = graph[element]
            for bag in outerBags:
                if (bag not in foundElements) and (bag not in elementsToAdd):
                    elementsToAdd.add(bag)
        if len(elementsToAdd) > 0:
            found = True
            foundElements.update(elementsToAdd)

    result = len(foundElements)
    print("EX1 result = ", result)
    return result

def getBagsFromGraph(graph, myBag):
    result = 1
    for (bag, counter) in graph[myBag].items():
        result += counter * getBagsFromGraph(graph, bag)
    return result

def ex2CalculateALlBags(data, myBag):
    graph = buildBagsGraph(data)
    result = getBagsFromGraph(graph, myBag) - 1

    print("EX2 Result = ", result)
    return result


if __name__ == "__main__":
    data = open("data.txt", "r").readlines()
    testData = open("test.txt", "r").readlines()

    assert ex1CalculateBagColors(testData, MY_BAG) == 4, "Something is wrong"
    assert ex1CalculateBagColors(data, MY_BAG) == 289

    assert ex2CalculateALlBags(testData, MY_BAG) == 32
    assert ex2CalculateALlBags(data, MY_BAG) == 30055
