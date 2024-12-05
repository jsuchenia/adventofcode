# Print Queue - https://adventofcode.com/2024/day/5

def get_data(filename: str) -> tuple[list[str], list[list[str]]]:
    with open(filename) as f:
        data = f.read().strip()
    rules, updates = data.split("\n\n")

    rules = rules.splitlines()
    updates = updates.splitlines()

    updates = [update.split(',') for update in updates]
    return rules, updates


def q1(filename: str) -> tuple[int, int]:
    rules, updates = get_data(filename)

    p1 = p2 = 0
    incorrect = []

    # part I
    for update in updates:
        for idx, page in enumerate(update):
            if any(f"{update[i]}|{page}" in rules for i in range(idx + 1, len(update))):
                incorrect.append(update)
                break
        else:
            p1 += int(update[len(update) // 2])

    # part II
    for update in incorrect:
        elements = set(update)
        result = []
        while elements:
            for element in elements:
                if not any(f"{other}|{element}" in rules for other in elements):
                    result.append(element)
                    elements.remove(element)
                    break

        p2 += int(result[len(result) // 2])
    return p1, p2


def test_q1_and_q2():
    assert q1("test.txt") == (143, 123)
    assert q1("data.txt") == (4814, 5448)
