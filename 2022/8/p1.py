def is_visible(grid, y, x):
    height = grid[y][x]

    # Visibility of other trees on a path in a direction - to be visible all needs to be smaller
    left = all(grid[z][x] < height for z in range(0, y))
    right = all(grid[z][x] < height for z in range(y + 1, len(grid)))
    up = all(grid[y][z] < height for z in range(0, x))
    down = all(grid[y][z] < height for z in range(x + 1, len(grid[y])))

    return up or down or left or right


def count_visible(file_name):
    with open(file_name) as f:
        data = f.readlines()

    grid = [[int(c) for c in list(line.strip())] for line in data]

    counter = 2 * len(grid) + len(grid[0]) + len(grid[-1]) - 4
    counter += sum(1 for y in range(1, len(grid) - 1) for x in range(1, len(grid[y]) - 1) if is_visible(grid, y, x))

    print(f"{counter=}")
    return counter


if __name__ == "__main__":
    assert count_visible("example.txt") == 21
    assert count_visible("data.txt") == 1662
