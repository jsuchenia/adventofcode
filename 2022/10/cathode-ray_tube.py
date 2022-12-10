def read_commands(file_name: str):
    with open(file_name) as f:
        return [line.strip().split(" ") for line in f.readlines()]


def run_program(file_name: str) -> (int, str):
    values, x = [], 1

    for cmd in read_commands(file_name):
        values.append(x)
        if cmd[0] == "addx":
            values.append(x)
            x += int(cmd[1])

    powersum = sum((idx + 1) * values[idx] for idx in range(19, len(values), 40))
    chars = ["X" if abs(val - i % 40) <= 1 else " " for i, val in enumerate(values)]

    print(f"{powersum=}")
    for idx in range(0, len(chars), 40):
        print("".join(chars[idx:idx + 40]))

    return powersum, "".join(chars)


if __name__ == "__main__":
    assert run_program("example.txt") == (13140,
                                          "XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  " +
                                          "XXX   XXX   XXX   XXX   XXX   XXX   XXX " +
                                          "XXXX    XXXX    XXXX    XXXX    XXXX    " +
                                          "XXXXX     XXXXX     XXXXX     XXXXX     " +
                                          "XXXXXX      XXXXXX      XXXXXX      XXXX" +
                                          "XXXXXXX       XXXXXXX       XXXXXXX     ")
    assert run_program("data.txt") == (14160,
                                       "XXX    XX XXXX XXX  XXX  XXXX XXXX  XX  " +
                                       "X  X    X X    X  X X  X X    X    X  X " +
                                       "X  X    X XXX  X  X X  X XXX  XXX  X    " +
                                       "XXX     X X    XXX  XXX  X    X    X    " +
                                       "X X  X  X X    X X  X    X    X    X  X " +
                                       "X  X  XX  XXXX X  X X    XXXX X     XX  ")
