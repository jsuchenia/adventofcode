# Print Queue - https://adventofcode.com/2024/day/5

def get_data(filename: str):
    with open(filename) as f:
        data = f.read().strip()
    rules, updates = data.split("\n\n")

    rules = rules.splitlines()
    updates = updates.splitlines()

    updates = [update.split(',') for update in updates]
    return rules, updates


def q1(filename: str) -> tuple[int, int]:
    rules, updates = get_data(filename)
    p1 = 0
    p2 = 0

    for update in updates:
        is_ok = True
        for idx, page in enumerate(update):
            for i in range(idx - 1):
                prev_page = update[i]
                rule = f"{page}|{prev_page}"

                if rule in rules:
                    is_ok = False

            for i in range(idx + 1, len(update)):
                next_page = update[i]
                rule = f"{next_page}|{page}"

                if rule in rules:
                    is_ok = False

        if is_ok:
            l = update[len(update) // 2]
            p1 += int(l)
        else:
            elements = set(update)
            result = []
            while elements:
                for element in elements:
                    is_ok = True
                    for other in elements:
                        if f"{other}|{element}" in rules:
                            is_ok = False
                    if is_ok:
                        result.append(element)
                        break
                elements.remove(result[-1])

            l = result[len(result) // 2]
            p2 += int(l)
    return p1, p2


def test_q1_and_q2():
    assert q1("test.txt") == (143, 123)
    assert q1("data.txt") == (4814, 5448)
