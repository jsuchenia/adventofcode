# Crossed Wires - https://adventofcode.com/2024/day/24
import re
from typing import Literal


def get_data(filename: str) -> tuple[dict[str, int], dict[str, tuple[str, ...]]]:
    with open(filename) as f:
        values, rules = f.read().strip().split("\n\n")

    values = {value.split(":")[0].strip(): int(value.split(":")[1]) for value in values.splitlines()}
    rules = [re.fullmatch(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)', rule) for rule in rules.splitlines()]
    rules = {rule[4]: (rule[1], rule[2], rule[3]) for rule in rules}
    return values, rules


def value(connecition: str, values: dict[str, int], rules: dict[str, tuple]) -> int:
    if connecition in values:
        return values[connecition]
    elif connecition in rules:
        left, op, right = rules[connecition]

        if op == "AND":
            return value(left, values, rules) & value(right, values, rules)
        elif op == "OR":
            return value(left, values, rules) | value(right, values, rules)
        elif op == "XOR":
            return value(left, values, rules) ^ value(right, values, rules)
        else:
            raise ValueError(f"Wrong operation {op}")
    else:
        raise ValueError(f"Unknown connection {connecition}")


def q1(filename: str) -> int:
    values, rules = get_data(filename)

    results = sorted([conn for conn in rules if conn.startswith("z")], reverse=True)
    result = ''.join([str(value(conn, values, rules)) for conn in results])
    return int(result, 2)


def test_q1():
    assert q1("test.txt") == 4
    assert q1("test2.txt") == 2024
    assert q1("data.txt") == 56939028423824


def test_zeros():
    values, rules = get_data("data.txt")

    zero_x = {f'x{i:02d}': 0 for i in range(45)}
    zero_y = {f'y{i:02d}': 0 for i in range(45)}

    results = sorted([conn for conn in rules if conn.startswith("z")], reverse=True)
    result = ''.join([str(value(conn, {**zero_x, **zero_y}, rules)) for conn in results])

    assert int(result, 2) == 0


def test_x_one():
    _, rules = get_data("data.txt")

    one_x = {f'x{i:02d}': 1 for i in range(45)}
    zero_y = {f'y{i:02d}': 0 for i in range(45)}
    values = {**one_x, **zero_y}

    results = sorted([conn for conn in rules if conn.startswith("z")], reverse=True)
    result = ''.join([str(value(conn, values, rules)) for conn in results])

    # Changes in a pattern
    assert value("z05", values, rules) == 0
    assert value("z16", values, rules) == 1
    assert value("z17", values, rules) == 0
    assert value("z39", values, rules) == 1

    assert result == '0111111000000000000000000000010000000000011111'


def test_y_one():
    _, rules = get_data("data.txt")

    zero_x = {f'x{i:02d}': 0 for i in range(45)}
    one_y = {f'y{i:02d}': 1 for i in range(45)}
    values = {**zero_x, **one_y}

    results = sorted([conn for conn in rules if conn.startswith("z")], reverse=True)
    result = ''.join([str(value(conn, values, rules)) for conn in results])

    # Changes in a pattern
    assert value("z05", values, rules) == 0
    assert value("z16", values, rules) == 1
    assert value("z17", values, rules) == 0
    assert value("z39", values, rules) == 1

    assert result == '0111111000000000000000000000010000000000011111'


def test_size_of_rules():
    values, rules = get_data("data.txt")

    assert len(values) == 2 * 45
    assert values["x44"] == 1
    assert values["y44"] == 1

    assert len(rules) == 5 * 45 - 3  # First adder don't have to implement r, z and c


def q2(filename: str) -> str:
    _, rules = get_data(filename)

    # Validate adder design
    # l1 = X XOR Y     # Intermediate sum
    # l2 = X AND Y     # Carry from X and Y
    # l3 = l1 AND Cin  # Carry from intermediate sum and Cin
    # z = l1 XOR Cin   # Final sum (Z)
    # c = l2 OR l3     # Final carry

    swapped: set[str] = set()
    found_rules: set[str] = set()

    def match_rule(left: str | None,
                   op: Literal['OR', 'XOR', 'AND'],
                   right: str | None,
                   output: str | None = None) -> str | None:

        for key, val in rules.items():
            # Exact search
            if val == (left, op, right) or val == (right, op, left):
                if output is not None and key != output:
                    swapped.update({key, output})
                found_rules.add(key)
                return key

        for key, val in rules.items():
            if val[1] == op:
                if val[0] == right or val[0] == left:
                    swapped.add(val[2])
                    found_rules.add(key)
                    return key
                if val[2] == right or val[2] == left:
                    swapped.add(val[0])
                    found_rules.add(key)
                    return key
        return None

    c = ""
    for i in range(45):
        if i == 0:  # First added is simple one - carry is always 0
            match_rule(f'x{i:02d}', "XOR", f'y{i:02d}', f"z{i:02d}")
            c = match_rule(f'x{i:02d}', "AND", f'y{i:02d}')
        else:
            l1 = match_rule(f'x{i:02d}', "XOR", f'y{i:02d}')
            l2 = match_rule(f'x{i:02d}', "AND", f'y{i:02d}')
            l3 = match_rule(c, 'AND', l1)
            match_rule(c, 'XOR', l1, f"z{i:02d}")
            c = match_rule(l3, "OR", l2)

    assert len(swapped) == 8, "Found exactly 8 swaps"
    assert len(rules) == len(found_rules), "Some rules has not been matched"

    return ','.join(sorted(swapped))


def test_q2():
    assert q2("data.txt") == 'frn,gmq,vtj,wnf,wtt,z05,z21,z39'
