from tqdm import tqdm

from monkey_test import read_data

CHECKPOINTS = {
    20: [99, 97, 8, 103],
    1000: [5204, 4792, 199, 5192],
    2000: [10419, 9577, 392, 10391],
    3000: [15638, 14358, 587, 15593],
    4000: [20858, 19138, 780, 20797],
    5000: [26075, 23921, 974, 26000],
    6000: [31294, 28702, 1165, 31204],
}

def play_game(file_name: str, factor: int) -> int:
    monkeys = read_data(file_name)

    for idx in range(1, 6001):
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

    print(f"FOOOOUND! {factor=}")
    return 0

if __name__ == "__main__":
    for factor in tqdm(range(1, 1_000_000)):
        if play_game("example.txt", factor) == 0:
            print(f"EUREKA! {factor=}")
            break
