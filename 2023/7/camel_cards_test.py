# Camel Cards
from collections import Counter

def get_data(filename: str) -> list[tuple[str, int]]:
    with open(filename) as f:
        lines = [line.split() for line in f.read().strip().splitlines()]

    return [(hand, int(bid)) for hand, bid in lines]

CARD_MAP_Q1 = {"T": "A", "J": "B", "Q": "C", "K": "D", "A": "E"}
CARD_MAP_Q2 = {"T": "A", "J": "1", "Q": "C", "K": "D", "A": "E"}
TYPES = [[1, 1, 1, 1, 1], [2, 1, 1, 1], [2, 2, 1], [3, 1, 1], [3, 2], [4, 1], [5]]

def get_type(hand: str) -> int:
    values = sorted(Counter(hand).values(), reverse=True)
    return TYPES.index(values)

def fix_joker_card(hand: str) -> str:
    if hand.count("J") == 5:
        return "AAAAA"
    counter = Counter(hand)
    del counter["J"]
    m = counter.most_common()[0][0]
    return hand.replace("J", m)

def encode_hand(cmap: dict[str, str], hand: str) -> str:
    return "".join([cmap.get(c, c) for c in hand])

def q1(filename: str) -> int:
    lines = get_data(filename)
    lines.sort(key=lambda line: (get_type(line[0]), encode_hand(CARD_MAP_Q1, line[0])))

    bids = [line[1] * idx for idx, line in enumerate(lines, start=1)]
    return sum(bids)

def q2(filename: str) -> int:
    lines = get_data(filename)
    lines.sort(key=lambda line: (get_type(fix_joker_card(line[0])), encode_hand(CARD_MAP_Q2, line[0])))

    bids = [line[1] * idx for idx, line in enumerate(lines, start=1)]
    return sum(bids)

def test_q1():
    assert q1("test.txt") == 6440
    assert q1("data.txt") == 253603890

def test_q2():
    assert q2("test.txt") == 5905
    assert q2("data.txt") == 253630098
