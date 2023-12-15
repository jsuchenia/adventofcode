import re

def read_data(filename: str):
    with open(filename) as f:
        lines = [line.rstrip() for line in f.readlines()]

    grove = lines[:-2]
    path = lines[-1]

    return re.findall(r"(\d+|R|L)", path), grove

MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def get_next_move2d(grove: list, point: tuple, move: int):
    x, y = point
    direction = MOVES[move]

    while True:
        y = (y + direction[1]) % len(grove)
        x = (x + direction[0]) % len(grove[y])

        if grove[y][x] in {".", "#"}:
            break

    return x, y

###### 150
#  12#
#  3 #
# 45 #
# 6  #
######
# 200
def get_next_move3d(grove: list, point: tuple, move: int):
    x, y = point
    direction = MOVES[move]
    x, y = x + direction[0], y + direction[1]

    if move == 0:  # right
        if x >= len(grove[y]) or grove[y][x] == " ":
            if y < 50:
                x = 99
                y = 149 - y
                move = 2
            elif 50 <= y < 100:
                x = 50 + y
                y = 49
                move = 3
            elif 100 <= y < 150:
                x = 149
                y = 149 - y
                move = 2
            elif 150 <= y:
                x = y - 100
                y = 149
                move = 3
    elif move == 2:  # left
        if x < 0 or grove[y][x] == " ":
            if y < 50:
                x = 0
                y = 149 - y
                move = 0
            elif 50 <= y < 100:
                x = y - 50
                y = 100
                move = 1
            elif 100 <= y < 150:
                x = 50
                y = 149 - y
                move = 0
            elif 150 <= y:
                x = y - 100
                y = 0
                move = 1
    elif move == 1:  # down
        if y >= len(grove) or x >= len(grove[y]) or grove[y][x] == " ":
            if x < 50:
                x = x + 100
                y = 0
            elif 50 <= x < 100:
                y = 100 + x
                x = 49
                move = 2
            elif 100 <= x:
                y = x - 50
                x = 99
                move = 2
    elif move == 3:  # up
        if y < 0 or grove[y][x] == " ":
            if x < 50:
                y = 50 + x
                x = 50
                move = 0
            elif 50 <= x < 100:
                y = 100 + x
                x = 0
                move = 0
            elif 100 <= x:
                x = x - 100
                y = 199
    return (x, y), move

def walk_over_map(filename: str, cube=False):
    move = 0
    path, grove = read_data(filename)

    pos = get_next_move2d(grove, (0, 0), move)
    for p in path:
        if p.isdigit():
            for _ in range(int(p)):
                if cube:
                    new_point, new_move = get_next_move3d(grove, pos, move)
                else:
                    new_point = get_next_move2d(grove, pos, move)
                    new_move = move

                if grove[new_point[1]][new_point[0]] == "#":
                    break

                pos = new_point
                move = new_move
        elif p == "R":
            move = (move + 1) % len(MOVES)
        elif p == "L":
            move = (move - 1) % len(MOVES)

    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + move

def test_monkey_map_example():
    assert walk_over_map("example.txt") == 6032

def test_monkey_map_data():
    assert walk_over_map("data.txt") == 75254

def test_monkey_map_data_with_bug():
    assert walk_over_map("data_with_bug.txt") == 75254

def test_monkey_map_p2_bug():
    assert walk_over_map("data_with_bug.txt", cube=True) == 112110

def test_monkey_map_p2_data():
    assert walk_over_map("data.txt", cube=True) == 108311
