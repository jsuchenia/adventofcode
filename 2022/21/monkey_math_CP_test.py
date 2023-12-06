# cpmpy require precision to be set, we used small precision previously
from functools import cache

from cpmpy import Model, intvar

def read_data(filename: str) -> list[list[str, str]]:
    with open(filename) as f:
        return [line.strip().split(":", maxsplit=1) for line in f.readlines()]


RANGE = 10**13


def estimate_humn_value(filename: str) -> int:
    monkeys = {monkey.strip(): op.strip() for monkey, op in read_data(filename)}
    human = intvar(-RANGE, RANGE, name="humn")

    @cache
    def get_symbol(monkey):
        if monkey == "humn":
            return human

        val = monkeys[monkey]
        if val.isdigit():
            return int(val)

        left = val[:4]
        right = val[7:]

        match val[5]:
            case "+":
                return get_symbol(left) + get_symbol(right)
            case "-":
                return get_symbol(left) - get_symbol(right)
            case "*":
                return get_symbol(left) * get_symbol(right)
            case "/":
                rs = get_symbol(right)
                ls = get_symbol(left)
                return ls // rs

    root = monkeys["root"]
    left_symbol = get_symbol(root[:4])
    right_symbol = get_symbol(root[7:])
    model = Model(left_symbol == right_symbol)
    if model.solve():
        result = human.value()
        print(f"P2: {filename=} {result=}")
        return result
    else:
        print("Can't solve!")


def test_monkey_math_cpmpy_example():
    assert estimate_humn_value("example.txt") == 301


def test_monkey_math_cpmpy_data():
    assert estimate_humn_value("data.txt") == 3330805295850
