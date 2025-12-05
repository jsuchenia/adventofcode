# Cafeteria - https://adventofcode.com/2025/day/5
from itertools import product


def get_data(filename: str) -> tuple[list[tuple[int, int]], list[int]]:
    with open(filename) as f:
        data = f.read().strip()

    # Process format
    rules_raw, ids_raw = data.split("\n\n")
    rules = [list(map(int, rule.strip().split('-'))) for rule in rules_raw.split("\n")]
    skus = [int(sku) for sku in ids_raw.split("\n")]

    # Compacting ranges...
    compacted_rules = []

    for start, end in sorted(rules, key=lambda rule: rule[0]):
        for i, (compact_start, compact_end) in enumerate(compacted_rules):
            if compact_start <= start <= compact_end or compact_start <= end <= compact_end:
                compacted_rules[i] = (min(start, compact_start), max(end, compact_end))
                break
        else:
            compacted_rules.append((start, end))
    return compacted_rules, skus


def q1(filename: str) -> int:
    rules, skus = get_data(filename)
    return len({sku for sku, rule in product(skus, rules) if rule[0] <= sku <= rule[1]})


def q2(filename: str) -> int:
    rules, _ = get_data(filename)
    return sum([stop - start + 1 for start, stop in rules])


def test_q1():
    assert q1("test.txt") == 3
    assert q1("data.txt") == 726


def test_q2():
    assert q2("test.txt") == 14
    assert q2("data.txt") == 354226555270043
