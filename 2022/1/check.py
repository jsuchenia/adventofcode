#!/usr/bin/env python
from pprint import pprint


def parse_file(file_name: str):
    with open(file_name, "r") as f:
        data = f.read()

    elves_str = data.split("\n\n")
    elves = [sum([int(v) for v in elve_values.split("\n")]) for elve_values in elves_str]
    return elves


def get_calories(file_name: str):
    data = parse_file(file_name)
    data.sort(reverse=True)

    return data[0], sum(data[0:3])


if __name__ == "__main__":
    assert get_calories("example.txt") == (24000, 45000)
    pprint(get_calories("data.txt"))
