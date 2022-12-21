def read_data(filename: str) -> list[list[str, str]]:
    with open(filename) as f:
        return [line.strip().split(":", maxsplit=1) for line in f.readlines()]


def get_root_value(filename: str):
    monkeys = {monkey.strip(): op.strip() for monkey, op in read_data(filename)}

    def get_value(monkey):
        val = monkeys[monkey]

        if val.isdigit():
            return int(val)

        left = val[:4]
        right = val[7:]

        match val[5]:
            case '+':
                return get_value(left) + get_value(right)
            case '-':
                return get_value(left) - get_value(right)
            case '*':
                return get_value(left) * get_value(right)
            case '/':
                return get_value(left) // get_value(right)

    result = get_value("root")
    print(f"P1 {filename=} {result=}")
    return result


if __name__ == "__main__":
    assert get_root_value("example.txt") == 152
    assert get_root_value("data.txt") == 145167969204648
