def read_data(filename: str) -> list[list[str, str]]:
    with open(filename) as f:
        return [line.strip().split(":", maxsplit=1) for line in f.readlines()]

def get_root_value(filename: str):
    monkeys = {monkey.strip(): op.strip() for monkey, op in read_data(filename)}

    # @cache - no need do cache, in both cases monkey was doing a computation only once
    def get_value(monkey):
        val = monkeys[monkey]

        if val.isdigit():
            return int(val)

        left = val[:4]
        right = val[7:]

        match val[5]:
            case "+":
                return get_value(left) + get_value(right)
            case "-":
                return get_value(left) - get_value(right)
            case "*":
                return get_value(left) * get_value(right)
            case "/":
                return get_value(left) // get_value(right)

    return get_value("root")

def test_monkey_math_p1_example():
    assert get_root_value("example.txt") == 152

def test_monkey_math_p1_data():
    assert get_root_value("data.txt") == 145167969204648
