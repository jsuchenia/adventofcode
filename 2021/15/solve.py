#!/usr/local/bin/python3

from collections import deque

def getdistances(graph, x, y):
    dist = {}
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
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
    val = src[y % len(src)][x % len(src[0])]
    dy = y//len(src)
    dx = x//len(src[0])
    nval = val + dx + dy
    if nval > 9:
        nval = (nval % 9)
    return nval

def buildmap2(lines, scale=5):
    src = [[int(val) for val in list(line.strip())] for line in lines]

    graph = [[getVal(src, x, y) for x in range(len(src[0]) * scale)] for y in range(len(src)*scale)]
    return graph


def scan(graph):
    distances = parsegraph(graph)
    pointcosts = {}

    q = deque()
    q.append((0, 0))
    pointcosts[(0, 0)] = 0

    while len(q) > 0:
        point = q.popleft()
        currentcost = pointcosts[point]

        for other, cost  in distances[point].items():
            newcost = currentcost + cost
            if (other not in pointcosts) or (pointcosts[other] > newcost):
                pointcosts[other] = newcost
                if other not in q: q.append(other)

    result = pointcosts[(len(graph[-1])-1, len(graph)-1)]
    print("Result =", result)
    return result


if __name__ == "__main__":
    test = open("test.txt", "r").read().splitlines()
    data = open("data.txt", "r").read().splitlines()
    mini = open("mini.txt", "r").read().splitlines()

    test1 = buildmap1(test)
    data1 = buildmap1(data)

    test2 = buildmap2(test)
    data2 = buildmap2(data)

    assert scan(test1) == 40
    assert scan(data1) == 363

    assert scan(test2) == 315
    assert scan(data2) == 2835
