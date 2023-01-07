#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/4

class Board:
    def __init__(self, index, boardStr):
        self.index = index
        self.skipped = False

        elements = []
        for line in boardStr:
            e = [int(line[x * 3:x * 3 + 2]) for x in range(5)]
            elements.extend(e)
        self.elements = elements
        self.match = [False] * 25

    def markNumber(self, number):
        try:
            i = self.elements.index(number)
            self.match[i] = True
        except ValueError:
            pass

    def checkRow(self, index):
        for i in range(5):
            if not self.match[5 * index + i]:
                return False
        print(self.index, "> Won row ", index, self.elements[5 * index:5 * (index + 1)])
        return True

    def checkColumn(self, index):
        for i in range(5):
            if not self.match[5 * i + index]:
                return False
        print(self.index, "> Won column", index, self.elements[index:25 + index:5])
        return True

    def checkBingo(self):
        for i in range(5):
            if self.checkRow(i):
                return True
            if self.checkColumn(i):
                return True
        return False

    def sumOtherNumbers(self, n):
        matches = [self.elements[x] for x in range(25) if self.match[x]]
        other = [self.elements[x] for x in range(25) if not self.match[x]]

        s = sum(other)
        result = s * n
        print(self.index, "> Matches ", matches)
        print(self.index, "> Other ", other)
        print(self.index, "> SUM", s)
        print(self.index, "> Result: ", result)

        return result

    def markAsSkipped(self):
        self.skipped = True

    def isSkipped(self):
        return self.skipped

def solve(filename):
    f = open(filename, "r")
    numbersStr = f.readline().split(",")
    numbers = [int(n) for n in numbersStr]
    f.readline()
    boardsStr = f.readlines()
    boards = []
    results = []

    for x in range(0, len(boardsStr), 6):
        boards.append(Board(x, boardsStr[x:x + 5]))

    for number in numbers:
        for board in boards:
            if not board.isSkipped():
                board.markNumber(number)
                if board.checkBingo():
                    results.append(board.sumOtherNumbers(number))
                    board.markAsSkipped()

    return results[0], results[-1]

def test_squid_example():
    assert solve("example.txt") == (4512, 1924)

def test_squid_data():
    assert solve("data.txt") == (14093, 17388)
