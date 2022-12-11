#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/1
def findPair(numbers, testing):
    for number in numbers:
        result = 2020 - testing
        pair = result - number
        if pair in numbers:
            print("Number is =", number, " pair = ", pair, " testing = ", testing)
            print("Result is: ", number * pair * testing)


if __name__ == "__main__":
    elements = open("data.txt", "r").read().splitlines()
    numbers = [int(n) for n in elements]

    print("======== EX 1 ========")
    findPair(numbers, 0)

    print("======== EX 2 ========")
    for number in numbers:
        findPair(numbers, number)
