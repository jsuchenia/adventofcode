import re

import pytest

def get_data(filename: str) -> dict[int, int]:
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    cards = {}

    for line in lines:
        card = int(re.match(r"Card\s+(\d+):", line)[1])

        numbers = line.split(":")[1]
        win_str, oth_str = numbers.split("|")
        win = set(int(n) for n in re.findall(r"(\d+)", win_str))
        oth = set(int(n) for n in re.findall(r"(\d+)", oth_str))

        cards[card] = len(win & oth)
    return cards

def q1(filename: str) -> int:
    cards = get_data(filename)
    results = [1 << (points - 1) for points in cards.values() if points]
    return sum(results)

def q2(filename: str) -> int:
    cards = get_data(filename)
    card_numbers = {card: 1 for card in cards.keys()}

    for card, points in cards.items():
        for new_card in range(card + 1, card + points + 1):
            card_numbers[new_card] += card_numbers[card]

    return sum(card_numbers.values())

@pytest.mark.parametrize("filename, result", [("test.txt", 13), ("data.txt", 20117)])
def test_q1(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test.txt", 30), ("data.txt", 13768818)])
def test_q2(filename: str, result: int):
    assert q2(filename) == result
