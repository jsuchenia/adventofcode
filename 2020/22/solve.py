#!/usr/local/bin/python3

from collections import deque
from itertools import islice


def parse(data):
    playerA, playerB = data.split("\n\n")

    player1 = [int(line) for line in playerA.splitlines()[1:]]
    player2 = [int(line) for line in playerB.splitlines()[1:]]

    return player1, player2


def calculateScore(cards):
    return sum([(i + 1) * card for i, card in enumerate(reversed(cards))])


def doGame(playerA, playerB, recursiveBattle, seengames, deep=0):
    cards1 = deque(playerA)
    cards2 = deque(playerB)

    marker = (tuple(cards1), tuple(cards2))
    if marker in seengames:
        print("Breaking simulation", marker)
        return cards1, []
    else:
        print("Adding marker", marker)
        seengames.add(marker)

    rounds = 0
    while len(cards1) > 0 and len(cards2) > 0:
        rounds += 1

        card1 = cards1.popleft()
        card2 = cards2.popleft()

        if recursiveBattle and (len(cards1) >= card1 and len(cards2) >= card2):
            print("Recursive battle mode")
            recPlayerA, recPlayerB = doGame(islice(cards1, 0, card1),
                                            islice(cards2, 0, card2),
                                            recursiveBattle=True,
                                            seengames=seengames,
                                            deep=deep + 1)

            if len(recPlayerA) > 0:
                cards1.extend((card1, card2))
            else:
                cards2.extend((card2, card1))
            continue

        if card1 > card2:
            cards1.extend((card1, card2))
        else:
            cards2.extend((card2, card1))

        if rounds % 200 == 199:
            print("{} - rounds tick - {} vs {}".format(rounds, cards1, cards2))

    print("{} > [{}] vs [{}]".format(deep, cards1, cards2))
    return cards1, cards2


def doCombat(data, recursiveBattle=False):
    playerA, playerB = parse(data)
    player1, player2 = doGame(playerA, playerB, recursiveBattle=recursiveBattle, seengames=set())

    if len(player1) > 0:
        result = calculateScore(player1)
    elif len(player2) > 0:
        result = calculateScore(player2)
    else:
        result = -1
    print("Simulation results", result)
    return result


if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    # assert doCombat(test) == 306
    # assert doCombat(str(data.txt.txt.txt.txt.txt.txt.txt.txt.txt.txt.txt.txt.txt.txt)) == 33631

    assert doCombat(test, recursiveBattle=True) == 291
    assert doCombat(data, recursiveBattle=True) == 33469
