import re


def read_data(file_name: str):
    with open(file_name) as f:
        data = f.read()

    status_raw, moves_raw = data.split("\n\n")

    # initial status
    status_pattern = re.compile(r'(\d+): (\w+)')
    status = [status_pattern.match(line).groups() for line in status_raw.split("\n")]
    status_map = {line[0]: line[1] for line in status}

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

    return ''.join([value[-1] for value in status.values()])


if __name__ == "__main__":
    assert do_moves("example.txt", reverse_order=True) == "CMZ"
    print(do_moves("data.txt", reverse_order=True))

    assert do_moves("example.txt", reverse_order=False) == "MCD"
    print(do_moves("data.txt", reverse_order=False))
