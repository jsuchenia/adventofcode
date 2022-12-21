# cpmpy fails:
# Also operations in cpmpy are limited.

from sympy import Integer, solve, Symbol, Eq


def read_data(filename: str) -> list[list[str, str]]:
    with open(filename) as f:
        return [line.strip().split(":", maxsplit=1) for line in f.readlines()]


def get_humn_value(filename: str) -> int:
    monkeys = {monkey.strip(): op.strip() for monkey, op in read_data(filename)}

    def get_symbol(monkey):
        if monkey == "humn":
            return Symbol("humn")

        val = monkeys[monkey]
        if val.isdigit():
            return Integer(int(val))

        left = val[:4]
        right = val[7:]

        match val[5]:
            case '+':
                return get_symbol(left) + get_symbol(right)
            case '-':
                return get_symbol(left) - get_symbol(right)
            case '*':
                return get_symbol(left) * get_symbol(right)
            case '/':
                return get_symbol(left) / get_symbol(right)

    root = monkeys["root"]
    left_symbol = get_symbol(root[:4])
    right_symbol = get_symbol(root[7:])
    result = solve(Eq(left_symbol, right_symbol))[0]
    print(f"P2: {filename=} {result=}")
    return result


if __name__ == "__main__":
    assert get_humn_value("example.txt") == 301
    assert get_humn_value("data.txt") == 3330805295850
