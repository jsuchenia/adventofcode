#!/usr/local/bin/python3
import re


def parse(data):
    res = re.compile(r"Player (\d+) starting position: (\d+)")
    return [int(p[1]) for p in res.findall(data)]


def get_predictive_dict_val(x):
    return ((x - 1) % 100) + 1


def get_dict_val(i):
    x = i % 100
    return sum([get_predictive_dict_val(3 * x + 1),
                get_predictive_dict_val((3 * x) + 2),
                get_predictive_dict_val((3 * x) + 3)])


def ex1(input_data):
    positions = parse(input_data)
    scores = [0] * len(positions)
    i = 0

    while True:
        idx = i % len(positions)
        value = get_dict_val(i)

        positions[idx] = ((positions[idx] + value - 1) % 10) + 1
        scores[idx] += positions[idx]

        if scores[idx] >= 1000:
            print("Break at round", i)
            dic_times = (3 * (i + 1))
            partner_score = scores[(idx + 1) % 2]
            result = dic_times * partner_score
            # print("Dic times", dic_times)
            # print("Partner score", partner_score)
            print("EX1> Result", result)
            return result
        i += 1


if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert ex1(test) == 739785
    assert ex1(data) == 893700
