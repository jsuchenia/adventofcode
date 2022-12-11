import math
from dataclasses import dataclass


@dataclass(kw_only=True)
class Monkey:
    items: list[int]
    operation: callable
    test_div: int
    div_true: int
    div_false: int
    counter: int = 0


def parse_monkey(data):
    lines = data.splitlines()
    return Monkey(
        items=[int(item) for item in lines[1].split(":")[1].strip().split(",")],
        operation=eval("lambda old: " + lines[2].split(":")[1].strip()[5:]),
        test_div=int(lines[3][21:].strip()),
        div_true=int(lines[4][29:].strip()),
        div_false=int(lines[5][30:].strip())
    )


def read_data(file_name: str):
    with open(file_name) as f:
        return [parse_monkey(monkey) for monkey in f.read().split("\n\n")]


def play_game(file_name: str, rounds: int, part_one: bool) -> int:
    monkeys = read_data(file_name)

    # From p2_brute.py and https://www.wolframalpha.com/input?i=96577 :)
    factor = math.lcm(*[monkey.test_div for monkey in monkeys])

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
    assert play_game("example.txt", rounds=20, part_one=True) == 10605
    assert play_game("data.txt", rounds=20, part_one=True) == 118674

    # P2 had different results for 20 rounds - clue for brute force
    assert play_game("example.txt", rounds=20, part_one=False) == 10197

    assert play_game("example.txt", rounds=10_000, part_one=False) == 2713310158
    assert play_game("data.txt", rounds=10_000, part_one=False) == 32333418600
