# Disk Fragmenter - https://adventofcode.com/2024/day/9

def get_data(filename: str) -> list[int]:
    with open(filename) as f:
        data = f.read().strip()
    return list(int(c) for c in data)


def q1(filename: str) -> int:
    data = get_data(filename)
    start = 0
    end = len(data)
    total = 0
    position = 0

    while start <= end:
        if start % 2 == 0:
            size = data[start]
            print(f"Block ID: {start // 2} with size {size}")
            total += sum(pos * start // 2 for pos in range(position, position + size))
            position += size
            start += 1
        elif end % 2 == 1:
            end -= 1
        elif data[start] == 0:
            start += 1
        elif data[end] == 0:
            end -= 1
        else:
            size = min(data[start], data[end])
            print(f"Block ID: {end // 2} with size {size}")
            total += sum(pos * end // 2 for pos in range(position, position + size))
            position += size

            data[start] -= size
            data[end] -= size

    return total


def q2(filename: str) -> int:
    data = get_data(filename)
    blocks = []

    for idx in range(len(data)):
        blocks.append((idx // 2 if idx % 2 == 0 else -1, data[idx]))

    for idx in range(len(blocks) - 1, 0, -1):
        block_id, block_size = blocks[idx]

        if block_id >= 0:
            for i in range(idx):
                if blocks[i][0] == -1 and blocks[i][1] >= block_size:
                    free_size = blocks[i][1] - block_size
                    blocks[idx] = (-1, block_size)
                    blocks[i] = (-1, free_size)
                    blocks.insert(i, (block_id, block_size))
                    break

    position = 0
    total = 0
    for block in blocks:
        if block[1] > 0 and block[0] >= 0:
            total += sum(pos * block[0] for pos in range(position, position + block[1]))
        position += block[1]
    return total


def test_q1():
    assert q1("test.txt") == 1928
    assert q1("data.txt") == 6398252054886


def test_q2():
    assert q2("test.txt") == 2858
    assert q2("data.txt") == 6415666220005
