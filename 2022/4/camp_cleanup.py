def get_pair(pair: str):
    p = tuple(int(num) for num in pair.split("-"))
    assert len(p) == 2
    assert p[0] <= p[1]
    return p


def parse_data_line(entry: str):
    pairs = tuple(get_pair(pair) for pair in entry.split(","))
    return pairs


def read_data(file_name: str):
    with open(file_name) as f:
        lines = [line.strip() for line in f.readlines()]
    return [parse_data_line(line) for line in lines]


def is_fully_overlaping(p):
    # A inside B or B inside A
    return p[0][0] >= p[1][0] and p[0][1] <= p[1][1] or p[1][0] >= p[0][0] and p[1][1] <= p[0][1]


def is_overlapping(p):
    # start A > end B = A completely bigger than B - no overlap
    # star B > end A = B completely bigger than A - no overlap
    return not (p[0][0] > p[1][1] or p[0][1] < p[1][0])


def count_overlaps(fileame: str):
    lines = read_data(fileame)
    full_overlaps = [is_fully_overlaping(line) for line in lines]
    partial_overlaps = [is_overlapping(line) for line in lines]
    return full_overlaps.count(True), partial_overlaps.count(True)


if __name__ == "__main__":
    assert count_overlaps("example.txt") == (2, 4)
    print(count_overlaps("data1.txt"))
