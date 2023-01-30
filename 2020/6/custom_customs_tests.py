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

def test_ex1_example():
    lines = open("example.txt", "r").read().splitlines()

    assert ex1(lines) == 6

def test_ex1_example2():
    lines = open("example2.txt", "r").read().splitlines()

    assert ex1(lines) == 11

def test_ex1():
    lines = open("data.txt", "r").read().splitlines()

    assert ex1(lines) == 6735

def test_ex2_example():
    lines = open("example2.txt", "r").read().splitlines()

    assert ex2(lines) == 6

def test_ex2():
    lines = open("data.txt", "r").read().splitlines()

    assert ex2(lines) == 3221
