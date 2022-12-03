#!/usr/bin/env python

def read_data(file_name: str):
    with open(file_name) as f:
        bags = [line.strip() for line in f.readlines()]
    return bags


def get_priority(letter):
    x = ord(letter)
    if x < ord('a'):
        return x - ord('A') + 27
    else:
        return x - ord('a') + 1


def calculate_priorities(file_name: str):
    bags = read_data(file_name)

    # Task 1 - find common between two parts
    divided_bags = [(bag[0:len(bag) // 2], bag[len(bag) // 2:]) for bag in bags]
    commons1 = [(set(bag1) & set(bag2)).pop() for bag1, bag2 in divided_bags]
    priorities1 = [get_priority(letter) for letter in commons1]

    # Task2 find common between 3 lines
    groups = [bags[idx:idx + 3] for idx in range(0, len(bags), 3)]
    commons2 = [(set(group[0]) & set(group[1]) & set(group[2])).pop() for group in groups]
    priorities2 = [get_priority(letter) for letter in commons2]

    return sum(priorities1), sum(priorities2)


if __name__ == "__main__":
    assert calculate_priorities("example.txt") == (157, 70)
    print(calculate_priorities("data.txt"))
