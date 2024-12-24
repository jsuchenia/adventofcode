# Crossed Wires - https://adventofcode.com/2024/day/24
import re


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
    values, rules = get_data(filename)

    # Validate adder design
    # l1 = X XOR Y     # Intermediate sum
    # l2 = X AND Y     # Carry from X and Y
    # l3 = l1 AND Cin  # Carry from intermediate sum and Cin
    # z = l1 XOR Cin   # Final sum (Z)
    # c = l2 OR l3     # Final carry

    def find_rule(left, op, right) -> str | None:
        for key, val in rules.items():
            if val == (left, op.upper(), right):
                return key
            if val == (right, op.upper(), left):
                return key
        return None

    swapped = []
    c = ""
    for i in range(45):
        l1 = find_rule(f'x{i:02d}', "XOR", f'y{i:02d}')
        l2 = find_rule(f'x{i:02d}', "AND", f'y{i:02d}')

        assert l1, f"Invalid L1 for x{i:02d} XOR y{i:02d}"
        assert l2, f"Invalid L1 for x{i:02d} AND y{i:02d}"

        if c:
            # Check L3 and z - both using l1
            # When both are wrong - probably l1 and l2 are swapped

            l3 = find_rule(c, 'AND', l1)
            z = find_rule(c, 'XOR', l1)

            if not l3 and not z:
                l3 = find_rule(c, 'AND', l2)
                z = find_rule(c, 'XOR', l2)
                assert l3, f"No l3 for {i=} {c=} {l2=}"
                assert z, f"Wrong z for {i=} {c=} {l2=}"

                l1, l2 = l2, l1
                swapped.extend([l1, l2])

            if l2.startswith("z") and not z.startswith("z"):
                l2, z = z, l2
                swapped.extend([l2, z])

            if l3.startswith("z") and not z.startswith("z"):
                l3, z = z, l3
                swapped.extend([l3, z])

            c = find_rule(l3, "OR", l2)
            assert c, f"No C for {i=} {l3=} {l2=}"

            if c.startswith("z") and not z.startswith("z"):
                swapped.extend([c, z])
                c, z = z, c
        else:
            c = l2

    assert len(swapped) == 8
    swapped.sort()
    return ','.join(swapped)


def test_q2():
    assert q2("data.txt") == 'frn,gmq,vtj,wnf,wtt,z05,z21,z39'
