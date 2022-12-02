#!/usr/bin/env python
from pprint import pprint


def get_data(file_name: str):
    with open(file_name, "r") as f:
        return [line.strip().split(" ") for line in f.readlines()]


# A for Rock, B for Paper, and C for Scissors (opponent)
# X for Rock, Y for Paper, and Z for Scissors (my move)

# 0 if you lost, 3 if the round was a draw, and 6 if you won

score1_table = {
    'A': {'X': 3, 'Y': 6, 'Z': 0},
    'B': {'X': 0, 'Y': 3, 'Z': 6},
    'C': {'X': 6, 'Y': 0, 'Z': 3}
}

# 1 for Rock, 2 for Paper, and 3 for Scissors
move1_score = {'X': 1, 'Y': 2, 'Z': 3}

# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
move2_score = {'X': 0, 'Y': 3, 'Z': 6}

score2_table = {
    'A': {'X': 3, 'Y': 1, 'Z': 2},
    'B': {'X': 1, 'Y': 2, 'Z': 3},
    'C': {'X': 2, 'Y': 3, 'Z': 1}
}

if __name__ == "__main__":
    data = get_data("data1.txt")
    pprint(data)

    score1 = [score1_table[opponent][you] + move1_score[you] for opponent, you in data]
    pprint(score1)
    pprint(sum(score1))

    score2 = [score2_table[opponent][you] + move2_score[you] for opponent, you in data]
    pprint(score2)
    pprint(sum(score2))
