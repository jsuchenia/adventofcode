# Bridge Repair - https://adventofcode.com/2024/day/7
from typing import Callable

import pytest


def get_data(filename: str) -> list[tuple[list[int], int]]:
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    ret = []
    for line in lines:
        target, vals = line.split(":")
        ret.append(([int(val) for val in vals.strip().split(" ")], int(target)))

    return ret


def is_valid_recur(vals, result, use_concatenation) -> bool:
    if len(vals) == 1:
        return vals[0] == result

    if vals[0] > result:
        return False

    if is_valid_recur([vals[0] * vals[1], *vals[2:]], result, use_concatenation):
        return True

    if use_concatenation and is_valid_recur([int(str(vals[0]) + str(vals[1])), *vals[2:]], result, use_concatenation):
        return True

    return is_valid_recur([vals[0] + vals[1], *vals[2:]], result, use_concatenation)


# Reverse check - we can validate additional checks for division and concatenation
def is_valid_reverse(vals, result, use_concatenation) -> bool:
    if len(vals) == 1:
        return vals[0] == result

    if (result % vals[-1]) == 0 and is_valid_reverse(vals[:-1], result // vals[-1], use_concatenation):
        return True

    if use_concatenation and result != vals[-1]:
        res_str = str(result)
        v_str = str(vals[-1])
        if res_str.endswith(v_str) and is_valid_reverse(vals[:-1], int(res_str[:-len(v_str)]), use_concatenation):
            return True

    if result >= vals[-1] and is_valid_reverse(vals[:-1], result - vals[-1], use_concatenation):
        return True

    return False


def q1(filename: str, method: Callable[[list[int], int, bool], bool]) -> int:
    data = get_data(filename)

    return sum(res for vals, res in data if method(vals, res, False))


def q2(filename: str, method: Callable[[list[int], int, bool], bool]) -> int:
    data = get_data(filename)

    return sum(res for vals, res in data if method(vals, res, True))


def test_q1_recur():
    assert q1("test.txt", is_valid_recur) == 3749
    assert q1("data.txt", is_valid_recur) == 8401132154762


def test_q1_reverse():
    assert q1("test.txt", is_valid_reverse) == 3749
    assert q1("data.txt", is_valid_reverse) == 8401132154762


@pytest.mark.skip("4sec vs 6ms in recur..")
def test_q2_recur():
    assert q2("test.txt", is_valid_recur) == 11387
    assert q2("data.txt", is_valid_recur) == 95297119227552


def test_q2_reverse():
    assert q2("test.txt", is_valid_reverse) == 11387
    assert q2("data.txt", is_valid_reverse) == 95297119227552
