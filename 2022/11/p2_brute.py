from dataclasses import dataclass

from tqdm import tqdm


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
    20: [99, 97, 8, 103],
    1000: [5204, 4792, 199, 5192],
    2000: [10419, 9577, 392, 10391],
    3000: [15638, 14358, 587, 15593],
    4000: [20858, 19138, 780, 20797],
    5000: [26075, 23921, 974, 26000],
    6000: [31294, 28702, 1165, 31204]
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
            if counters != CHECKPOINTS[idx]:
                return -1
            print(f"Probably good factor {factor=} {idx=}")

    print(f"FOOOOUND! {factor=}")
    return 0


if __name__ == "__main__":
    for factor in tqdm(range(1, 1_000_000)):
        if play_game("example.txt", factor) == 0:
            print(f"EUREKA! {factor=}")
            break
