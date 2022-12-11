#!/usr/local/bin/python3
ALL_CHARS = "abcdefghijklmnopqrstuvwxyz"


def ex1(lines):
    acc = set()
    total = 0

    for line in lines:
        if line:
            for c in line:
                acc.add(c)
        else:
            total += len(acc)
            acc = set()
    total += len(acc)
    return total


def ex2(lines):
    acc = set(ALL_CHARS)
    total = 0

    for line in lines:
        if line:
            for c in ALL_CHARS:
                if (c not in line) and (c in acc):
                    acc.remove(c)
        else:
            total += len(acc)
            acc = set(ALL_CHARS)
    total += len(acc)
    return total


if __name__ == "__main__":
    lines = open("data.txt", "r").read().splitlines()

    assert ex1(lines) == 6735
    assert ex2(lines) == 3221
