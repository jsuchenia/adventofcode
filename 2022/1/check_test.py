#!/usr/bin/env python


def parse_file(file_name: str):
    with open(file_name, "r") as f:
        data = f.read()

    elves_str = data.split("\n\n")
    return [sum([int(v) for v in elve_values.split("\n")]) for elve_values in elves_str]

def get_calories(file_name: str):
    data = parse_file(file_name)
    data.sort(reverse=True)

    return (data[0], sum(data[0:3]))

def test_calories_example():
    assert get_calories("example.txt") == (24000, 45000)

def test_calories_data():
    assert get_calories("data.txt") == (69693, 200945)
