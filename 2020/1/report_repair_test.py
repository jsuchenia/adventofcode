#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/1
import itertools
import math

def find_pair(filename: str, size: int) -> int:
    elements = open(filename, "r").read().splitlines()
    numbers = {int(n) for n in elements}

    for pair in itertools.combinations(numbers, size):
        if sum(pair) == 2020:
            result = math.prod(pair)
            print(f"{result=}")
            return result

def test_sum_p1_example():
    assert find_pair("example.txt", size=2) == 514579

def test_sum_p1_data():
    assert find_pair("data.txt", size=2) == 898299

def test_sum_p2_example():
    assert find_pair("example.txt", size=3) == 241861950

def test_sum_p2_data():
    assert find_pair("data.txt", size=3) == 143933922
