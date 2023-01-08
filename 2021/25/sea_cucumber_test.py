#!/usr/local/bin/python3
from copy import deepcopy

def ex1(filename):
    data = open(filename, "r").read()
    map = [list(line) for line in data.splitlines()]
    step = 0

    while True:
        moved = False
        newmap = deepcopy(map)
        step += 1

        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == '>' and map[y][(x + 1) % len(map[y])] == '.':
                    newmap[y][x] = '.'
                    newmap[y][(x + 1) % len(map[y])] = '>'
                    moved = True
        map = deepcopy(newmap)
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == 'v' and map[(y + 1) % len(map)][x] == '.':
                    newmap[y][x] = '.'
                    newmap[(y + 1) % len(map)][x] = 'v'
                    moved = True

        map = deepcopy(newmap)
        # print("-------------", step)
        # for line in map:
        #     print(''.join(line))
        if not moved:
            print("Step not moved", step)
            return step

def test_game_of_live_test():
    assert ex1("test.txt") == 58

def test_game_of_live_data():
    assert ex1("data.txt") == 563
