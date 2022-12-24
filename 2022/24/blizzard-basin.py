from collections import deque


def read_data(filename):
    with open(filename) as f:
        lines = [row[1:-1] for row in f.read().splitlines()[1:-1]]
    valley = {(x, y): point for y, i in enumerate(lines) for x, point in enumerate(i)}

    return valley, len(lines), len(lines[0])


MOVES = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]


def do_bfs(valley, rows, cols, start, end, start_time):
    def is_empty(p, t):
        x, y = p

        if valley[(x, (y - t) % rows)] == "v" or valley[(x, (y + t) % rows)] == "^":
            return False
        if valley[((x - t) % cols, y)] == ">" or valley[((x + t) % cols, y)] == "<":
            return False
        return True

    visited = set()
    bfs = deque([(start, start_time)])

    while bfs:
        state = bfs.popleft()
        if state in visited:
            continue
        visited.add(state)

        pos, time = state

        for move in MOVES:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            new_state = (new_pos, time + 1)

            if new_pos == end:
                print(f"{new_state=}")
                return new_state[1]

            if new_pos == end or new_pos == start or (new_pos in valley and is_empty(*new_state)):
                bfs.append(new_state)

    raise ValueError("Can't find BFS path")


def p1(filename):
    valley, rows, cols = read_data(filename)
    start = (0, -1)
    end = (cols - 1, rows)
    return do_bfs(valley, rows, cols, start, end, 0)


def p2(filename):
    valley, rows, cols = read_data(filename)
    start = (0, -1)
    end = (cols - 1, rows)
    t1 = do_bfs(valley, rows, cols, start, end, 0)
    t2 = do_bfs(valley, rows, cols, end, start, t1)
    t3 = do_bfs(valley, rows, cols, start, end, t2)

    print(f"{t1=} {t2=} {t3=}")
    return t3


if __name__ == "__main__":
    assert p1("example.txt") == 18
    assert p1("data.txt") == 253

    assert p2("example.txt") == 54
    assert p2("data.txt") == 794
