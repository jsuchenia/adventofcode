import re
from collections import defaultdict

import pytest

def read_data(filename: str):
    pattern = re.compile(r"=(-?\d+)")
    with open(filename) as f:
        return [map(int, pattern.findall(line)) for line in f.readlines()]

def count_cover_line(filename: str, line: int) -> int:
    data = read_data(filename)
    beacons = set()
    coverage = set()

    for xs, ys, xb, yb in data:
        distance = abs(xs - xb) + abs(ys - yb)
        line_distance = abs(line - ys)

        if line_distance > distance:
            continue
        spray = abs(line_distance - distance)
        xmin = xs - spray
        xmax = xs + spray

        for x in range(xmin, xmax + 1):
            coverage.add(x)
        if yb == line:
            beacons.add(xb)
    size = len(coverage) - len(beacons)
    print(f"{filename=} Coverage: {len(coverage)} Beacons: {len(beacons)} {size=}")
    return size

def find_missing_spot(filename: str, max_range: int) -> int:
    data = read_data(filename)
    line_coverage = defaultdict(list)

    for xs, ys, xb, yb in data:
        distance = abs(xs - xb) + abs(ys - yb)
        ymin = max(ys - distance, 0)
        ymax = min(ys + distance, max_range)

        for line in range(ymin, ymax + 1):
            line_distance = abs(line - ys)
            spray = abs(line_distance - distance)
            xmin = max(xs - spray, 0)
            xmax = min(xs + spray, max_range)
            line_coverage[line].append((xmin, xmax))

    print(f"{filename=} Coverage created, now checking consistency!")
    for line, coverage in line_coverage.items():
        coverage.sort(key=lambda x: x[0])
        x = 0
        for c in coverage:
            xmin, xmax = c

            if xmin > x + 1:
                print(f"{filename=} Found inconsistency! - p=({x + 1}, {line})")
                freq = (x + 1) * 4000000 + line
                print(f"{filename=} {freq=}")
                return freq
            x = max(x, xmax)
        if x < max_range:
            print("Not covered line!?", x, line)
            return 0
    return 0

def test_exclusion_zone_count_line_example():
    assert count_cover_line("example.txt", line=10) == 26

@pytest.mark.skip(reason="It uses too much memory (more than 1GiB) NUC")
def test_exclusion_zone_count_line_data():
    assert count_cover_line("data.txt", line=2_000_000) == 5809294

def test_find_missing_spot_example():
    assert find_missing_spot("example.txt", max_range=20) == 56000011

@pytest.mark.skip(reason="Memory limit (more than 1GiB)")
def test_find_missing_spot_data():
    assert find_missing_spot("data.txt", max_range=4_000_000) == 10693731308112
