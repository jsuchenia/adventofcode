#!/usr/local/bin/python3
from collections import defaultdict, Counter
from math import prod

MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

def parse(data):
    tiles = {}
    for entry in data.split("\n\n"):
        lines = entry.splitlines()
        tiles[int(lines[0][5:-1])] = lines[1:]
    return tiles

def encodeBorder(border):
    return int(border.replace(".","0").replace("#", "1"),2)

def encodeTile(tile):
    borders = [tile[0], tile[-1], ''.join(row[0] for row in tile), ''.join(row[-1] for row in tile)]
    markers = set()
    for border in borders:
        markers.update([encodeBorder(border), encodeBorder(border[::-1])])
    return markers

def doCheck(data):
    tiles = parse(data)
    borderMatches = defaultdict(list)

    for tileid,tile in tiles.items():
        for marker in encodeTile(tile):
            borderMatches[marker].append(tileid)

    borderCounter = Counter()
    for marker, tileIds in borderMatches.items():
        if len(tileIds) == 1:
            borderCounter.update(tileIds)

    corners = [mc[0] for mc in borderCounter.most_common(4)]
    print("Found corners", corners)
    result = prod(corners)
    print("Result is", result)
    return result

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert doCheck(test) == 20899048083289
    assert doCheck(data) == 14986175499719