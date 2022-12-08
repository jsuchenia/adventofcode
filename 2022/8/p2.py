def get_score(grid, y, x):
    height = grid[y][x]
    
    # Distance to visible trees (or to the edge)
    up = [y - z for z in range(y - 1, -1, -1) if grid[z][x] >= height] + [y]
    down = [z - y for z in range(y + 1, len(grid)) if grid[z][x] >= height] + [len(grid) - y - 1]
    left = [x - z for z in range(x - 1, -1, -1) if grid[y][z] >= height] + [x]
    right = [z - x for z in range(x + 1, len(grid[y])) if grid[y][z] >= height] + [len(grid[y]) - x - 1]

    # Only first (visible) distance used for score
    return up[0] * down[0] * left[0] * right[0]


def get_max_score(file_name: str):
    with open(file_name) as f:
        data = f.readlines()

    grid = [[int(c) for c in list(line.strip())] for line in data]
    scores = [get_score(grid, y, x) for y in range(1, len(grid) - 1) for x in range(1, len(grid[y]) - 1)]
    max_score = max(scores)
    print(f"{max_score=}")
    return max_score


if __name__ == "__main__":
    assert get_max_score("example.txt") == 8
    assert get_max_score("data.txt") == 537600
