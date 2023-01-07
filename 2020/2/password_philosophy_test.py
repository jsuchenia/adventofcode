#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/2
import re

def read_data(filename):
    pattern = re.compile(r"^(\d+)-(\d+) (\w): (\w+)$")
    with open(filename, "r") as f:
        for line in f.read().splitlines():
            g = pattern.match(line).groups()
            yield int(g[0]), int(g[1]), g[2], g[3]

def valid_entries_p1(filename):
    return sum([1 for lmin, lmax, letter, password in read_data(filename) if lmin <= password.count(letter) <= lmax])

def valid_entries_p2(filename):
    result = 0
    for lmin, lmax, letter, password in read_data(filename):
        l1 = password[lmin - 1]
        l2 = password[lmax - 1]

        if l1 != l2 and (l1 == letter or l2 == letter):
            result += 1

    print(f"{result=}")
    return result

def test_p1_example():
    assert valid_entries_p1("example.txt") == 2

def test_p1_data():
    assert valid_entries_p1("data.txt") == 580

def test_p2_example():
    assert valid_entries_p2("example.txt") == 1

def test_p2_data():
    assert valid_entries_p2("data.txt") == 611
