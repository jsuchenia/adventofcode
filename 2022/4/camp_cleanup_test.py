import re

PATTERN = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

def read_data(file_name: str):
    with open(file_name) as f:
        return [[int(x) for x in PATTERN.match(line).groups()] for line in f.readlines()]

def is_fully_overlapping(points):
    # A inside B or B inside A
    return points[0] >= points[2] and points[1] <= points[3] or \
           points[2] >= points[0] and points[3] <= points[1]

def is_overlapping(points):
    # start A > end B = A completely bigger than B - no overlap
    # star B > end A = B completely bigger than A - no overlap
    return not (points[0] > points[3] or
                points[1] < points[2])

def count_overlaps(fileame: str):
    lines = read_data(fileame)

    full_overlaps = [is_fully_overlapping(points) for points in lines]
    partial_overlaps = [is_overlapping(points) for points in lines]

    result = (full_overlaps.count(True), partial_overlaps.count(True))
    print(f"{result=}")
    return result

def test_count_overlapp_example():
    assert count_overlaps("example.txt") == (2, 4)

def test_count_overlapp_data():
    assert count_overlaps("data.txt") == (547, 843)
