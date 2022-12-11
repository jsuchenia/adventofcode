import math
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


def play_game(file_name: str, rounds: int, part_one: bool) -> int:
    monkeys = read_data(file_name)

    # From p2_brute.py and https://www.numberempire.com/96577 :)
    factor = math.prod([monkey.test_div for monkey in monkeys])

    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items:
                new = monkey.operation(item)
                if part_one:
                    new //= 3
                new %= factor
                dst_monkey = monkey.div_false if new % monkey.test_div else monkey.div_true
                monkeys[dst_monkey].items.append(new)
            monkey.counter += len(monkey.items)
            monkey.items.clear()

    counters = sorted([monkey.counter for monkey in monkeys], reverse=True)
    score = math.prod(counters[:2])
    print(f"{score=}")
    return score


if __name__ == "__main__":
    assert play_game("example1.txt", rounds=20, part_one=True) == 10605
    assert play_game("data.txt", rounds=20, part_one=True) == 118674
    assert play_game("example1.txt", rounds=10_000, part_one=False) == 2713310158
    assert play_game("data.txt", rounds=10_000, part_one=False) == 32333418600
