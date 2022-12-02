#!/usr/bin/env python
from pprint import pprint

# A for Rock, B for Paper, and C for Scissors (opponent)
# X for Rock, Y for Paper, and Z for Scissors (my move)

# 0 if you lost, 3 if the round was a draw, and 6 if you won
# 1 for Rock, 2 for Paper, and 3 for Scissors
score1_table = {
    'A': {'X': 3 + 1, 'Y': 6 + 2, 'Z': 0 + 3},
    'B': {'X': 0 + 1, 'Y': 3 + 2, 'Z': 6 + 3},
    'C': {'X': 6 + 1, 'Y': 0 + 2, 'Z': 3 + 3}
}

# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
score2_table = {
    'A': {'X': 3, 'Y': 1 + 3, 'Z': 2 + 6},
    'B': {'X': 1, 'Y': 2 + 3, 'Z': 3 + 6},
    'C': {'X': 2, 'Y': 3 + 3, 'Z': 1 + 6}
}


def get_scores(file_name: str):
    with open(file_name, "r") as f:
        data = [line.strip().split(" ") for line in f.readlines()]

    score1 = sum([score1_table[opponent][you] for opponent, you in data])
    score2 = sum([score2_table[opponent][you] for opponent, you in data])

    return score1, score2


if __name__ == "__main__":
    assert get_scores("example.txt") == (15, 12)
    pprint(get_scores("data1.txt"))
