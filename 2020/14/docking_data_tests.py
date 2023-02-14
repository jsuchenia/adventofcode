#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/14
import re
from itertools import product

def parseMask(pattern):
    mask_or = int(pattern.replace("X", "0"), 2)
    mask_and = int(pattern.replace("X", "1"), 2)

    return mask_or, mask_and

def allIdx(idx, mask):
    assert len(mask) == 36
    idxStr = "{0:036b}".format(idx)
    assert len(idxStr) == 36

    pattern = []

    for i in range(36):
        if mask[i] == '0':
            pattern.append(idxStr[i])
        elif mask[i] == '1':
            pattern.append('1')
        elif mask[i] == 'X':
            pattern.append(['0', '1'])
        else:
            print("DUPA, ERROR")
    assert len(pattern) == 36
    return [int(x, 2) for x in [''.join(p) for p in product(*pattern)]]

def ex2(data):
    pat = re.compile("mem\[(\d+)\] = (\d+)")
    values = {}
    mask = ""

    for line in data:
        if line.startswith("mask"):
            mask = line[7:]
        elif line.startswith("mem"):
            res = pat.match(line)
            for idx in allIdx(int(res.group(1)), mask):
                values[idx] = int(res.group(2))
    result = sum(values.values())
    print("EX2 result =", result)
    return result

def ex1(data):
    mask_or = mask_and = 0
    values = {}

    pat = re.compile("mem\[(\d+)\] = (\d+)")

    for line in data:
        if line.startswith("mask"):
            pattern = line[7:]
            mask_or, mask_and = parseMask(pattern)
        elif line.startswith("mem"):
            res = pat.match(line)
            val = (int(res.group(2)) | mask_or) & mask_and
            values[int(res.group(1))] = val

    result = sum(values.values())
    print("Result =", result)
    return result

def test_program_test():
    test = open("test.txt", "r").read().splitlines()
    assert ex1(test) == 165

def test_program_test2():
    test2 = open("test2.txt", "r").read().splitlines()
    assert ex1(test2) == 51

def test_program_data():
    data = open("data.txt", "r").read().splitlines()
    assert ex1(data) == 10885823581193

def test_program_v2_test2():
    test2 = open("test2.txt", "r").read().splitlines()
    assert ex2(test2) == 208

def test_program_v2_data():
    data = open("data.txt", "r").read().splitlines()
    assert ex2(data) == 3816594901962
