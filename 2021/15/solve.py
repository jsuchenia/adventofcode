#!/usr/local/bin/python3

from heapq import heappop, heappush
import matplotlib.pyplot as plt

def getdistances(graph, x, y):
    dist = {}
    for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy
        if x == nx and y == ny: continue
        if ny < 0 or ny >= len(graph): continue
        if nx < 0 or nx >= len(graph[ny]): continue

        point = (nx, ny)
        dist[point] = graph[ny][nx]
    return dist

def parsegraph(graph):
    distances = {}
    for y in range(len(graph)):
        for x in range(len(graph[y])):
            point = (x, y)
            distances[point] = getdistances(graph, x, y)
    return distances

def buildmap1(lines):
    return [[int(val) for val in list(line.strip())] for line in lines]

def getVal(src, x, y):
    srcy = y % len(src)
    srcx = x % len(src[srcy])
    val = src[srcy][srcx]
    dy = y//len(src)
    dx = x//len(src[srcy])
    nval = val + dx + dy
    if nval > 9:
        nval -= 9
    return nval

def buildmap2(lines, scale=5):
    src = [[int(val) for val in list(line.strip())] for line in lines]

    graph = [[getVal(src, x, y) for x in range(len(src[0]) * scale)] for y in range(len(src)*scale)]
    return graph

def scan(graph, visualization = False):
    distances = parsegraph(graph)
    pointcosts = {}

    DST=(len(graph[-1]) - 1, len(graph) - 1)
    START=(0, 0)

    min_dst_costs = 9 * (DST[0] + DST[1]) # diagonal walk over only 9ines, pessimistic approach

    q = [(0, START)]
    pointcosts[START] = 0

    if visualization:
        plt.axis([0, len(graph[-1]), 0, len(graph)])

    while len(q) > 0:
        _, point = heappop(q)

        currentcost = pointcosts[point]

        if currentcost > min_dst_costs:
            continue

        for other, cost in distances[point].items():
            newcost = currentcost + cost
            if newcost > min_dst_costs:
                continue

            if (other not in pointcosts) or (pointcosts[other] > newcost):
                pointcosts[other] = newcost

                if other == DST:
                    min_dst_costs = newcost
                else:
                    heappush(q, (newcost, other))

        if visualization:
            plt.scatter(point[0], point[1])
            plt.pause(0.000001)

    print("Result =", min_dst_costs)
    return min_dst_costs

if __name__ == "__main__":
    test = open("test.txt", "r").read().splitlines()
    data = open("data.txt", "r").read().splitlines()

    test1 = buildmap1(test)
    data1 = buildmap1(data)

    test2 = buildmap2(test)
    data2 = buildmap2(data)

    assert scan(test1, visualization=False) == 40
    assert scan(data1) == 363

    assert scan(test2) == 315
    assert scan(data2) == 2835
