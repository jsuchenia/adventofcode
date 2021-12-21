#!/usr/local/bin/python3
import re

def parse(data):
    res = re.compile("Player (\d+) starting position: (\d+)")
    return res.findall(data)

def getDicVal(x):
    return ((x-1)%100)+1

def getDiceValue(round):
    x = round % 100
    return sum([getDicVal(3 * x + 1), getDicVal((3 * x) + 2), getDicVal((3 * x) + 3)])

def ex1(data):
    startPositions = parse(data)
    positions = [int(p[1]) for p in startPositions]
    scores = [0] * len(positions)
    round = 0

    while True:
        idx = round % len(positions)
        value = getDiceValue(round)

        positions[idx] = ((positions[idx] + value-1) % 10) + 1
        print("New position for IDX", idx+1, positions[idx])
        scores[idx] += positions[idx]
        print("Score of player {} is {}".format(idx+1, scores[idx]))

        if scores[idx] >= 1000:
            print("Break at round", round)
            dicTimes = (3*(round+1))
            partnerScore = scores[(idx+1)%2]
            result = dicTimes * partnerScore
            print("Dic times", dicTimes)
            print("Partner score", partnerScore)
            print("Result", result)
            return result
        round += 1

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert ex1(test) == 739785
    assert ex1(data) == 893700
