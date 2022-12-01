#!/usr/bin/env python


def parse_file(file_name: str):
    with open(file_name, "r") as f:
        data = f.read()

    elves_str = data.split("\n\n")
    elves = [sum([int(v) for v in elve_values.split("\n")]) for elve_values in elves_str]
    return elves


if __name__ == "__main__":
    elves = parse_file("data")
    elves.sort(reverse=True)
    print("Task one", elves[0])
    print("Task two", sum(elves[0:3]))
