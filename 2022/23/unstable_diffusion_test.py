from collections import defaultdict


def read_data(filename: str) -> set[tuple[int, int]]:
    field = set()
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            for x, val in enumerate(line.strip()):
                if val == "#":
                    field.add((x, y))

    return field


def do_scan(filename: str, repeats: int = 10, stop_when_not_moved: bool = False) -> int:
    orig = read_data(filename)

    ADJACENT = lambda x, y: [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    MOVES = [
        lambda x, y: [(x, y - 1), (x - 1, y - 1), (x + 1, y - 1)],  # N, NE, NW
        lambda x, y: [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)],  # S, SE, SW
        lambda x, y: [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1)],  # W, NW, SW
        lambda x, y: [(x + 1, y), (x + 1, y - 1), (x + 1, y + 1)],  # E, NE, SE
    ]

    field = orig.copy()

    for i in range(repeats):
        propositions = defaultdict(int)
        prop_per_elf = {}

        # Round I
        for elf in field:
            if all(p not in field for p in ADJACENT(*elf)):
                continue

            for move in MOVES:
                positions = move(*elf)
                if all(p not in field for p in positions):
                    prop_per_elf[elf] = positions[0]
                    propositions[positions[0]] += 1
                    break

        dst_field = set()

        for elf in field:
            p = prop_per_elf.get(elf, None)

            if p and propositions[p] == 1:
                dst_field.add(p)
            else:
                dst_field.add(elf)

        MOVES.append(MOVES.pop(0))

        # for y in range(min_y, max_y + 1):
        #     for x in range(min_x, max_x + 1):
        #         if (x, y) in dst_field:
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print(" ")
        # print("\n")

        if stop_when_not_moved and field == dst_field:
            print(f"Not moved in round {i + 1}")
            return i + 1

        field = dst_field

    min_x = min(x for x, y in field)
    max_x = max(x for x, y in field)
    min_y = min(y for x, y in field)
    max_y = max(y for x, y in field)

    result = (max_x - min_x + 1) * (max_y - min_y + 1) - len(field)
    print(f"{result=}")
    return result


def test_unstable_diffusion_p1_small():
    assert do_scan("small.txt", repeats=10) == 25


def test_unstable_diffusion_p1_example():
    assert do_scan("example.txt", repeats=10) == 110


def test_unstable_diffusion_p1_data():
    assert do_scan("data.txt", repeats=10) == 4000


def test_unstable_diffusion_p2_example():
    assert do_scan("example.txt", repeats=30, stop_when_not_moved=True) == 20


def test_unstable_diffusion_p2_data():
    assert do_scan("data.txt", repeats=2000, stop_when_not_moved=True) == 1040
