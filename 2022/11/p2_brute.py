from dataclasses import dataclass


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: callable
    test_div: int
    div_true: int
    div_false: int
    counter: int = 0


def parse_monkey(data):
    lines = data.splitlines()
    id = lines[0][7:-1]
    items = [int(item) for item in lines[1].split(":")[1].strip().split(",")]
    operation = eval("lambda old: " + lines[2].split(":")[1].strip()[5:])
    div_by = int(lines[3][21:].strip())
    div_true = int(lines[4][29:].strip())
    div_false = int(lines[5][30:].strip())

    return Monkey(id=id, items=items, operation=operation, test_div=div_by, div_true=div_true, div_false=div_false)


def read_data(file_name: str):
    with open(file_name) as f:
        monkeys = f.read().split("\n\n")

    return [parse_monkey(monkey) for monkey in monkeys]


CHECKPOINTS = {
    1: [2, 4, 3, 6],
    20: [99, 97, 8, 103],
    1000: [5204, 4792, 199, 5192]
}


def play_game(file_name: str, factor: int) -> int:
    monkeys = read_data(file_name)

    for idx in range(1, 4001):
        for monkey in monkeys:
            for item in monkey.items:
                new = monkey.operation(item)
                # new /= factor
                new %= factor
                dst_monkey = monkey.div_false if new % monkey.test_div else monkey.div_true
                monkeys[dst_monkey].items.append(new)
            monkey.counter += len(monkey.items)
            monkey.items = []

        counters = [monkey.counter for monkey in monkeys]
        if idx in CHECKPOINTS:
            for a, b in zip(counters, CHECKPOINTS[idx]):
                if a != b:
                    return -1
            if idx > 1:
                print(f"Probably good factor {factor=} {idx=}")

    print(f"FOOOOUND! {factor=}")
    return 0


if __name__ == "__main__":
    for factor in range(1, 1_000_000):
        if factor % 1000 == 0:
            print(f"Checking {factor=}")

        if play_game("example.txt", factor) == 0:
            print(f"EUREKA! {factor=}")
            break
