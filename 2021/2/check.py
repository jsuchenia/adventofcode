#!/usr/local/bin/python3

def ex1(data):
    position = 0
    depth = 0

    for entry in data:
        if entry.startswith("forward "):
            position += int(entry[8:])
        elif entry.startswith("down "):
            depth += int(entry[5:])
        elif entry.startswith("up "):
            depth -= int(entry[3:])
        else:
            print("Unknown command", entry)

    print("[ex1] Position =", position)
    print("[ex1] Depth =", depth)
    print("[ex1] Solution1 = ", position * depth)

def ex2(data):
    aim = 0
    depth = 0
    position = 0

    for entry in data:
        if entry.startswith("forward "):
            position += int(entry[8:])
            depth += (aim * int(entry[8:]))
        elif entry.startswith("down "):
            aim += int(entry[5:])
        elif entry.startswith("up "):
            aim -= int(entry[3:])
        else:
            print("Unknown command", entry)

    print("ex2> Position =", position)
    print("ex2> Depth =", depth)
    print("ex2> Solution = ", position * depth)

if __name__ == "__main__":
    data = open("data", "r").readlines()
    ex1(data)
    ex2(data)