#!/usr/local/bin/python3

def checkSlopes(lines, right, down):
    position = 0
    treeCounter = 0
    lineIndex = 0

    while lineIndex < len(lines):
        line = lines[lineIndex].strip()
        if line[position] == '#':
            treeCounter += 1

        position = (position + right) % 31
        lineIndex += down

    print("Right = ", right, ", down = ", down, ", total trees = ", treeCounter)
    return treeCounter


if __name__ == "__main__":
    lines = open("data").read().splitlines()

    result = checkSlopes(lines, 1, 1)
    result *= checkSlopes(lines, 3, 1)
    result *= checkSlopes(lines, 5, 1)
    result *= checkSlopes(lines, 7, 1)
    result *= checkSlopes(lines, 1, 2)

    print("Total result = ", result)
