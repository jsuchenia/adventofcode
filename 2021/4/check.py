#!/usr/local/bin/python3
import sys

class Board:
    def __init__(self, index, boardStr):
        self.index = index
        self.skipped = False

        elements = []
        for line in boardStr:
            e = [int(line[x*3:x*3+2]) for x in range(5)]
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
            if not self.match[5*index+i]:
                return False
        print(self.index,"> Won row ", index, self.elements[5*index:5*(index+1)])
        return True

    def checkColumn(self, index):
        for i in range(5):
            if not self.match[5*i+index]:
                return False
        print(self.index, "> Won column", index, self.elements[index:25+index:5])
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
        print(self.index, "> Matches ", matches)
        print(self.index, "> Other ", other)
        print(self.index, "> SUM", s)
        print(self.index, "> Result: ", s * n)

    def markAsSkipped(self):
        self.skipped = True

    def isSkipped(self):
        return self.skipped

if __name__ == "__main__":
    f = open("data", "r")
    numbersStr = f.readline().split(",")
    numbers = [ int(n) for n in numbersStr]
    f.readline()
    boardsStr = f.readlines()
    boards = []

    for x in range(0, len(boardsStr), 6):
        boards.append(Board(x, boardsStr[x:x+5]))

    for number in numbers:
        print("Checking ", number)

        for board in boards:
            if not board.isSkipped():
                board.markNumber(number)
                if board.checkBingo():
                    board.sumOtherNumbers(number)
                    board.markAsSkipped()
    print("No bingo, something is wrong")
