#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/13
from itertools import groupby

def dump(points):
    result = "\n"
    for y, row in groupby(sorted(points, key=lambda x: x[1]), lambda x: x[1]):
        all_x = [point[0] for point in row]
        result += ''.join(['#' if i in all_x else ' ' for i in range(0, max(all_x) + 1)])
        result += '\n'
    return result

def parse(data):
    (dataLines, commandLines) = data.split("\n\n")
    commands = commandLines.splitlines()
    points = set(tuple(map(int, line.split(","))) for line in dataLines.splitlines())
    return points, commands

def do_task(filename, run_all=False):
    data = open(filename, "r").read()

    points, commands = parse(data)

    for cmd in commands:
        fold_value = int(cmd[13:])
        axis = 1 if cmd[11] == 'y' else 0
        points = {tuple(min(2 * fold_value - val, val) if i == axis else val for i, val in enumerate(point)) for point in points}
        if not run_all: break

    result = len(points)
    print("EX{}> Finally we have {} points".format("2" if run_all else "1", result))

    if run_all:
        return result, dump(points)

    return result

def test_origami_ex1_test():
    assert do_task("test.txt") == 17

def test_origami_ex1_data():
    assert do_task("data.txt") == 827

def test_origami_ex2_test():
    assert do_task("test.txt", run_all=True) == (16, '''
#####
#   #
#   #
#   #
#####
''')

def test_origami_ex2_data():
    assert do_task("data.txt", run_all=True) == (104, '''
####  ##  #  # #  # ###  ####  ##  ###
#    #  # #  # # #  #  # #    #  # #  #
###  #  # #### ##   #  # ###  #    #  #
#    #### #  # # #  ###  #    #    ###
#    #  # #  # # #  # #  #    #  # #
#### #  # #  # #  # #  # ####  ##  #
''')
