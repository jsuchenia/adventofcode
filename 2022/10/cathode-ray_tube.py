def read_commands(file_name: str):
    with open(file_name) as f:
        return [line.strip().split(" ") for line in f.readlines()]


def run_program(file_name: str):
    cmds = read_commands(file_name)

    values = []
    x = 1

    for cmd in cmds:
        values.append(x)
        if cmd[0] == "addx":
            values.append(x)
            x += int(cmd[1])

    powersum = sum((idx + 1) * values[idx] for idx in range(19, len(values), 40))
    print(f"{powersum=}")

    chars = ["X" if abs(values[idx] - idx % 40) <= 1 else " " for idx in range(0, len(values))]
    for idx in range(0, len(chars), 40):
        print("".join(chars[idx:idx + 40]))

    return powersum


if __name__ == "__main__":
    assert run_program("example.txt") == 13140
    assert run_program("data.txt") == 14160
