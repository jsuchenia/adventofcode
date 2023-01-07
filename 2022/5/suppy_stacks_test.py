import re

def read_data(file_name: str):
    with open(file_name) as f:
        data = f.read()

    status_raw, moves_raw = data.split("\n\n")

    # Parse matrix...
    matrix_lines = status_raw.split('\n')

    # Locate indexes in a last line
    indexes = {char: i for i, char in enumerate(matrix_lines[-1]) if char.isdigit()}
    status_map = {char: "" for char in indexes.keys()}

    # Iterate over matrix in a reverse order
    for line in matrix_lines[0:-1][::-1]:
        for char, idx in indexes.items():  # Locate cel for each index
            if idx < len(line) and line[idx] != " ":
                status_map[char] += line[idx]
    # moves
    moves_pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    moves = [moves_pattern.match(line).groups() for line in moves_raw.split("\n")]
    return status_map, moves

def do_moves(file_name: str, reverse_order=True):
    status, moves = read_data(file_name)

    for move in moves:
        size, src, dst = int(move[0]), move[1], move[2]

        transport = status[src][-size:]
        status[src] = status[src][0:-size]
        status[dst] += transport[::-1] if reverse_order else transport

    result = ''.join([value[-1] for value in status.values()])
    print(f"{result=}")
    return result

def test_moves_p1_example():
    assert do_moves("example.txt") == "CMZ"

def test_moves_p1_data():
    assert do_moves("data.txt") == "FWNSHLDNZ"

def test_moves_p2_example():
    assert do_moves("example.txt", reverse_order=False) == "MCD"

def test_moves_p2_data():
    assert do_moves("data.txt", reverse_order=False) == "RNRGDNFQG"
