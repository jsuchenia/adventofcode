# sympy version - we are tracking back a whole computation
# Sympy can do it better, but boolean values and constrains are harder to add

from sympy import Eq, Symbol, simplify, solve


def read_data(filename: str) -> list[list[str, str]]:
    with open(filename) as f:
        return [line.strip().split(":", maxsplit=1) for line in f.readlines()]


def estimate_humn_value(filename: str) -> int:
    monkeys = {monkey.strip(): op.strip() for monkey, op in read_data(filename)}

    # @cache
    def get_symbol(monkey):
        if monkey == "humn":
            return Symbol("h")

        val = monkeys[monkey]
        if val.isdigit():
            return int(val)

        left = val[:4]
        right = val[7:]

        match val[5]:
            case "+":
                return simplify(get_symbol(left) + get_symbol(right))
            case "-":
                return simplify(get_symbol(left) - get_symbol(right))
            case "*":
                return simplify(get_symbol(left) * get_symbol(right))
            case "/":
                return simplify(get_symbol(left) / get_symbol(right))

    root = monkeys["root"]
    left_symbol = get_symbol(root[:4])
    right_symbol = get_symbol(root[7:])
    return int(solve(Eq(left_symbol, right_symbol))[0])


def test_monkey_math_sympy_p2_example():
    assert estimate_humn_value("example.txt") == 301


def test_monkey_math_sympy_p2_data():
    assert estimate_humn_value("data.txt") == 3330805295850
