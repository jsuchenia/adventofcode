#!/usr/local/bin/python3
import re

def parse(data):
    res = re.compile(r"Player (\d+) starting position: (\d+)")
    return [int(p[1]) for p in res.findall(data)]

def getDicVal(x):
    return ((x-1)%100)+1

def getDiceValue(round):
    x = round % 100
    return sum([getDicVal(3 * x + 1), getDicVal((3 * x) + 2), getDicVal((3 * x) + 3)])

def ex1(data):
    positions = parse(data)
    scores = [0] * len(positions)
    round = 0

    while True:
        idx = round % len(positions)
        value = getDiceValue(round)

        positions[idx] = ((positions[idx] + value-1) % 10) + 1
        scores[idx] += positions[idx]

        if scores[idx] >= 1000:
            print("Break at round", round)
            dicTimes = (3*(round+1))
            partnerScore = scores[(idx+1)%2]
            result = dicTimes * partnerScore
            # print("Dic times", dicTimes)
            # print("Partner score", partnerScore)
            print("EX1> Result", result)
            return result
        round += 1

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert ex1(test) == 739785
    assert ex1(data) == 893700
