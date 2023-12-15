from collections import deque

def get_data(filename: str):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def get_elevation(chr):
    if chr == "S":
        return 0
    elif chr == "E":
        return 25
    else:
        return ord(chr) - ord("a")

def get_available_childs(data, y, x, reverse) -> list:
    moves = []

    elevation = get_elevation(data[y][x])
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy

        if 0 <= ny < len(data) and 0 <= nx < len(data[ny]):
            next_elevation = get_elevation(data[ny][nx])
            if (not reverse and next_elevation <= elevation + 1) or (reverse and next_elevation >= elevation - 1):
                moves.append((nx, ny))
    return moves

def build_graph(data, reverse):
    graph, starts, end = {}, [], None

    for y in range(len(data)):
        for x in range(len(data[y])):
            char = data[y][x]
            pos = (x, y)
            graph[pos] = get_available_childs(data, y, x, reverse)

            if char == "S":
                starts.insert(0, pos)
            elif char == "E":
                end = pos
            elif char == "a":
                starts.append(pos)
    return graph, starts, end

def bfs(graph, *, root, ends):
    queue = deque()
    visited = set()
    final = set(ends)

    queue.append((0, root))
    visited.add(root)

    while queue:
        weight, node = queue.popleft()

        for child in graph[node]:
            if child in final:
                return weight + 1

            if child not in visited:
                visited.add(child)
                if child in graph:
                    queue.append((weight + 1, child))

def count_steps_from_end(filename: str) -> int:
    data = get_data(filename)
    graph, starts, end = build_graph(data, reverse=True)
    min_score = bfs(graph, root=end, ends=starts)

    return min_score

def count_steps_from_start(filename: str) -> int:
    data = get_data(filename)
    graph, starts, end = build_graph(data, reverse=False)

    score = bfs(graph, root=starts[0], ends=[end])

    return score

def test_cont_steps_p1_example():
    assert count_steps_from_start("example.txt") == 31

def test_cont_steps_p1_data():
    assert count_steps_from_start("data.txt") == 490

def test_cont_steps_p2_example():
    assert count_steps_from_end("example.txt") == 29

def test_cont_steps_p2_data():
    assert count_steps_from_end("data.txt") == 488
