#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/1

def ex2(filename):
    data = [int(x) for x in open(filename, 'r').readlines()]
    datalen = len(data)
    sums = [data[i] + data[i + 1] + data[i + 2] for i in range(datalen - 2)]
    counter = len([1 for i in range(1, len(sums)) if (sums[i] > sums[i - 1])])
    print("[Excercise 2] ", counter)
    return counter

def ex1(filename):
    data = [int(x) for x in open(filename, 'r').readlines()]
    counter = len([1 for i in range(1, len(data)) if (data[i] > data[i - 1])])
    print("[Excercise 1] ", counter)
    return counter

def test_sonar_p1_example():
    assert ex1("example.txt") == 7

def test_sonar_p1_data():
    assert ex1("data.txt") == 1665

def test_sonar_p2_example():
    assert ex2("example.txt") == 5

def test_sonar_p2_data():
    assert ex2("data.txt") == 1702
