#!/usr/bin/env python3
# https://adventofcode.com/2021/day/23

import math
from functools import cache
from heapq import heappop, heappush

CORRIDOR = "..........."

CONNECTIONS_PART1 = {
    0: [{"to": 1, "steps": 1}],
    1: [{"to": 11, "steps": 2, "onlyFor": 'A'}, {"to": 0, "steps": 1}, {"to": 3, "steps": 2}],
    2: [],
    3: [{"to": 11, "steps": 2, "onlyFor": 'A'}, {"to": 13, "steps": 2, "onlyFor": 'B'}, {"to": 1, "steps": 2},
        {"to": 5, "steps": 2}],
    4: [],
    5: [{"to": 13, "steps": 2, "onlyFor": 'B'}, {"to": 15, "steps": 2, "onlyFor": 'C'}, {"to": 3, "steps": 2},
        {"to": 7, "steps": 2}],
    6: [],
    7: [{"to": 15, "steps": 2, "onlyFor": 'C'}, {"to": 17, "steps": 2, "onlyFor": 'D'}, {"to": 5, "steps": 2},
        {"to": 9, "steps": 2}],
    8: [],
    9: [{"to": 17, "steps": 2, "onlyFor": 'D'}, {"to": 7, "steps": 2}, {"to": 10, "steps": 1}],
    10: [{"to": 9, "steps": 1}],

    # Room A
    11: [{"to": 12, "steps": 1, "onlyFor": 'A', "blocking": True}, {"to": 1, "steps": 2}, {"to": 3, "steps": 2}],
    12: [{"to": 11, "steps": 1}],

    # Room B
    13: [{"to": 14, "steps": 1, "onlyFor": 'B', "blocking": True}, {"to": 3, "steps": 2}, {"to": 5, "steps": 2}],
    14: [{"to": 13, "steps": 1}],

    # Room C
    15: [{"to": 16, "steps": 1, "onlyFor": 'C', "blocking": True}, {"to": 5, "steps": 2}, {"to": 7, "steps": 2}],
    16: [{"to": 15, "steps": 1}],

    # Room D
    17: [{"to": 18, "steps": 1, "onlyFor": 'D', "blocking": True}, {"to": 7, "steps": 2}, {"to": 9, "steps": 2}],
    18: [{"to": 17, "steps": 1}],
}
CONNECTIONS_PART2 = {
    0: [{"to": 1, "steps": 1}],
    1: [{"to": 0, "steps": 1}, {"to": 3, "steps": 2}, {"to": 11, "steps": 2, "onlyFor": 'A'}],
    2: [],
    3: [{"to": 1, "steps": 2}, {"to": 5, "steps": 2}, {"to": 11, "steps": 2, "onlyFor": 'A'},
        {"to": 15, "steps": 2, "onlyFor": 'B'}],
    4: [],
    5: [{"to": 3, "steps": 2}, {"to": 7, "steps": 2}, {"to": 15, "steps": 2, "onlyFor": 'B'},
        {"to": 19, "steps": 2, "onlyFor": 'C'}],
    6: [],
    7: [{"to": 5, "steps": 2}, {"to": 9, "steps": 2}, {"to": 19, "steps": 2, "onlyFor": 'C'},
        {"to": 23, "steps": 2, "onlyFor": 'D'}],
    8: [],
    9: [{"to": 7, "steps": 2}, {"to": 10, "steps": 1}, {"to": 23, "steps": 2, "onlyFor": 'D'}],
    10: [{"to": 9, "steps": 1}],

    # Room A
    11: [{"to": 1, "steps": 2}, {"to": 3, "steps": 2}, {"to": 12, "steps": 1, "onlyFor": 'A', "blocking": True}],
    12: [{"to": 11, "steps": 1}, {"to": 13, "steps": 1, "onlyFor": 'A', "blocking": True}],
    13: [{"to": 12, "steps": 1}, {"to": 14, "steps": 1, "onlyFor": 'A', "blocking": True}],
    14: [{"to": 13, "steps": 1}],

    # Room B
    15: [{"to": 3, "steps": 2}, {"to": 5, "steps": 2}, {"to": 16, "steps": 1, "onlyFor": 'B', "blocking": True}],
    16: [{"to": 15, "steps": 1}, {"to": 17, "steps": 1, "onlyFor": 'B', "blocking": True}],
    17: [{"to": 16, "steps": 1}, {"to": 18, "steps": 1, "onlyFor": 'B', "blocking": True}],
    18: [{"to": 17, "steps": 1}],

    # Room C
    19: [{"to": 5, "steps": 2}, {"to": 7, "steps": 2}, {"to": 20, "steps": 1, "onlyFor": 'C', "blocking": True}],
    20: [{"to": 19, "steps": 1}, {"to": 21, "steps": 1, "onlyFor": 'C', "blocking": True}],
    21: [{"to": 20, "steps": 1}, {"to": 22, "steps": 1, "onlyFor": 'C', "blocking": True}],
    22: [{"to": 21, "steps": 1}],

    # Room D
    23: [{"to": 7, "steps": 2}, {"to": 9, "steps": 2}, {"to": 24, "steps": 1, "onlyFor": 'D', "blocking": True}],
    24: [{"to": 23, "steps": 1}, {"to": 25, "steps": 1, "onlyFor": 'D', "blocking": True}],
    25: [{"to": 24, "steps": 1}, {"to": 26, "steps": 1, "onlyFor": 'D', "blocking": True}],
    26: [{"to": 25, "steps": 1}]
}

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def genNewState(state, src, dst):
    newstate = list(state)

    c = newstate[src]
    newstate[src] = '.'
    newstate[dst] = c

    return ''.join(newstate)


def checkIfFinal(idx, state, finishState, connections):
    if idx < 11:
        return False

    if state[idx] != finishState[idx]:
        return False

    for conn in connections[idx]:
        if (not "blocking" in conn) or (not conn["blocking"]):
            continue

        if not checkIfFinal(conn["to"], state, finishState, connections):
            return False

    return True


@cache
def getDiffPriority(state, finalState):
    return math.prod([10 if state[idx] != finalState[idx] else 1 for idx in range(len(finalState))])


def doSimul(startState, finishState, connections):
    q = [(0, startState)]
    minConsts = {startState: 0}

    ITER_ORDER = list(reversed(range(len(finishState))))

    while len(q) > 0:
        print("Len", len(q))
        priority, state = heappop(q)

        initConst = minConsts[state]

        if finishState in minConsts and minConsts[finishState] < initConst:
            continue

        for idx in ITER_ORDER:
            c = state[idx]
            if c == '.':
                continue
            if checkIfFinal(idx, state, finishState, connections):
                continue

            conns = connections[idx]

            if len(conns) == 0:
                print("INVALID STATE:", state)
                return -1

            for conn in conns:
                to = conn["to"]

                if state[to] != '.':
                    continue

                if "onlyFor" in conn and c not in conn["onlyFor"]:
                    continue

                newcosts = initConst + (conn["steps"] * COSTS[c])
                newstate = genNewState(state, idx, to)

                if finishState in minConsts and minConsts[finishState] < newcosts:
                    continue

                if newstate in minConsts and minConsts[newstate] <= newcosts:
                    continue

                minConsts[newstate] = newcosts
                priority = getDiffPriority(newstate[11:], finishState[11:])
                heappush(q, (priority, newstate))

    print("Simulation {} finished!".format(startState))
    result = minConsts[finishState]
    print("Result is", result)
    return result


def ex1(startState):
    FINAL_STATE = CORRIDOR + "AABBCCDD"

    return doSimul(startState, FINAL_STATE, CONNECTIONS_PART1)


def ex2(startState):
    FINAL_STATE = CORRIDOR + "AAAABBBBCCCCDDDD"

    return doSimul(startState, FINAL_STATE, CONNECTIONS_PART2)


if __name__ == "__main__":
    # assert ex1(CORRIDOR + "BACDBCDA") == 12521
    # assert ex1(CORRIDOR + "DBACDBCA") == 14348
    # assert ex2(CORRIDOR + "BDDACCBDBBACDACA") == 44169
    assert ex2(CORRIDOR + "DDDBACBCDBABCACA") == 14348
