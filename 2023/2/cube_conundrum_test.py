import re
from collections import Counter, defaultdict
from math import prod

import pytest

type Colors = dict[str, int]

# class Colors(TypedDict):
#     green: int
#     blue: int
#     red: int


def get_data(filename: str) -> dict[int, Colors]:
    with open(filename, "r") as f:
        lines = f.readlines()

    games: dict[int, Colors] = {}

    for line in lines:
        game_id = int(re.match(r"^Game (\d+):", line)[1])

        max_elements: Colors = defaultdict(int)
        for n, color in re.findall(r"(\d+) (\w+)", line):
            max_elements[color] = max(max_elements[color], int(n))

        games[game_id] = max_elements
    return games

def q1(filename: str) -> int:
    games = get_data(filename)

    limits = Counter({"red": 12, "green": 13, "blue": 14})
    game_ids = [game_id for game_id, elements in games.items() if Counter(elements) < limits]

    return sum(game_ids)

def q2(filename: str) -> int:
    games = get_data(filename)
    powers = [prod(elements.values()) for elements in games.values()]

    return sum(powers)

@pytest.mark.parametrize("filename, result", [("test1.txt", 8), ("data.txt", 2727)])
def test_q1_test(filename: str, result: int):
    assert q1(filename) == result

@pytest.mark.parametrize("filename, result", [("test1.txt", 2286), ("data.txt", 56580)])
def test_q2_test(filename: str, result: int):
    assert q2(filename) == result
