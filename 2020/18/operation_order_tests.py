#!/usr/local/bin/python3
from io import StringIO

OPERATORS = {'+', '*'}

def parse(s):
    elements = []
    while c := s.read(1):
        if c == "" or c == ")":
            break

        if c in OPERATORS:
            elements.append(c)
        elif c == " ":
            continue
        elif c == "(":
            elements.append(parse(s))
        elif c.isdigit():
            while n := s.read(1):
                if n.isdigit():
                    c += n
                else:
                    s.seek(s.tell() - 1)
                    break
            elements.append(int(c))
    return elements

def reduceAddition(expr):
    i = 1
    while i < len(expr):
        if expr[i] == '+':
            left = expr[i - 1]
            if type(left) is list:
                left = evaluate(left, True)
            right = expr[i + 1]
            if type(right) is list:
                right = evaluate(right, True)

            expr[i - 1] = left + right
            del expr[i]
            del expr[i]
        else:
            i += 2

def evaluate(expr, precedence):
    if precedence:
        reduceAddition(expr)

    left = expr.pop(0)

    if type(left) is list:
        left = evaluate(left, precedence)

    while len(expr) > 0:
        op = expr.pop(0)
        right = expr.pop(0)

        if type(right) is list:
            right = evaluate(right, precedence)

        if op == "+":
            left += right
        elif op == "*":
            left *= right
        else:
            print("UNSUPPORTED OPERATION", op)
            break

    return left

def solve(data, precedence=False):
    result = 0
    for line in data:
        s = StringIO(line)
        e = parse(s)
        print(e)
        val = evaluate(e, precedence)
        print(val)
        result += val
    print("Result: ", result)
    return result

def test_order_example():
    assert solve(["1 + 2 * 3 + 4 * 5 + 6"]) == 71
    assert solve(["1 + (2 * 3) + (4 * (5 + 6))"]) == 51
    assert solve(["2 * 3 + (4 * 5)"]) == 26
    assert solve(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]) == 437
    assert solve(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]) == 12240
    assert solve(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]) == 13632

def test_order():
    data = open("data.txt", "r").read().splitlines()
    assert solve(data) == 3647606140187

def test_order_with_precedence_example():
    assert solve(["1 + 2 * 3 + 4 * 5 + 6"], True) == 231
    assert solve(["1 + (2 * 3) + (4 * (5 + 6))"], True) == 51
    assert solve(["2 * 3 + (4 * 5)"], True) == 46
    assert solve(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], True) == 669060

def test_order_with_precedence():
    data = open("data.txt", "r").read().splitlines()
    assert solve(data, True) == 323802071857594
