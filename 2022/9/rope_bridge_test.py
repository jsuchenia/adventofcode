MOVES = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}


def read_data(file_name: str):
    with open(file_name) as f:
        moves = f.readlines()
    steps = [line.strip().split(" ") for line in moves]
    return [(MOVES[a], int(b)) for a, b in steps]


def count_tail_positions(file_name, rope_length) -> int:
    moves = read_data(file_name)

    rope = [(0, 0)] * rope_length
    visited = set()

    for move, count in moves:
        for _ in range(count):
            rope[0] = (rope[0][0] + move[0], rope[0][1] + move[1])
            for idx in range(1, len(rope)):
                diff = (rope[idx - 1][0] - rope[idx][0], rope[idx - 1][1] - rope[idx][1])
                if abs(diff[0]) > 1 or abs(diff[1]) > 1:
                    step = (min(1, max(-1, diff[0])), min(1, max(-1, diff[1])))
                    rope[idx] = (rope[idx][0] + step[0], rope[idx][1] + step[1])
            visited.add(rope[rope_length - 1])

    print(f"Visited len {file_name=} {rope_length=}: {len(visited)}")
    return len(visited)


def test_count_p1_example():
    assert count_tail_positions("example.txt", rope_length=2) == 13


def test_count_p1_data():
    assert count_tail_positions("data.txt", rope_length=2) == 6175


def test_count_p2_example():
    assert count_tail_positions("example.txt", rope_length=10) == 1


def test_count_p2_example2():
    assert count_tail_positions("example2.txt", rope_length=10) == 36


def test_count_p2_data():
    assert count_tail_positions("data.txt", rope_length=10) == 2578
