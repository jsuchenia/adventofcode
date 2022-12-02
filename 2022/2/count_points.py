#!/usr/bin/env python
from pprint import pprint

# Common:
# A for Rock, B for Paper, and C for Scissors (opponent)
# X for Rock, Y for Paper, and Z for Scissors (my move)

# Points
# 0 if you lost, 3 if the round was a draw, and 6 if you won
# 1 for Rock, 2 for Paper, and 3 for Scissors

# Case 2:
# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win

# Points calculated from a matrix (then matrix simplified)
points1 = [3, 6, 0]
points2 = [3, 1, 2]


def get_scores(file_name: str):
    with open(file_name, "r") as f:
        data = [line.strip().split(" ") for line in f.readlines()]
    num = [(ord(x[0]) - ord('A'), ord(x[1]) - ord('X')) for x in data]

    score1 = sum([points1[(n[1] - n[0]) % 3] + n[1] + 1 for n in num])
    score2 = sum([points2[(n[1] + n[0]) % 3] + 3 * n[1] for n in num])

    return score1, score2


if __name__ == "__main__":
    assert get_scores("example.txt") == (15, 12)
    pprint(get_scores("data1.txt"))
