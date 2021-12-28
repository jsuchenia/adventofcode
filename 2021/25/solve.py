#!/usr/local/bin/python3
from copy import deepcopy

def ex1(data):
    map = [list(line) for line in data.splitlines()]
    step = 0

    for line in map:
        print(''.join(line))

    while True:
        moved = False
        newmap = deepcopy(map)
        step += 1

        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == '>' and map[y][(x+1) % len(map[y])] == '.':
                    newmap[y][x] = '.'
                    newmap[y][(x+1) % len(map[y])] = '>'
                    moved = True
        map = deepcopy(newmap)
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == 'v' and map[(y+1) % len(map)][x] == '.':
                    newmap[y][x] = '.'
                    newmap[(y+1) % len(map)][x] = 'v'
                    moved = True

        map = deepcopy(newmap)
        print("-------------", step)
        for line in map:
            print(''.join(line))
        if not moved:
            print("Step not moved", step)
            return step
        else:
            print("Step moved - next loop", step)

if __name__ == "__main__":
    test = open("test.txt", "r").read()
    data = open("data.txt", "r").read()

    assert ex1(test) == 58
    assert ex1(data) == 563