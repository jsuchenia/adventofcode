#!/usr/local/bin/python3

class Table:
    def __init__(self, input):
        self.table = self.parse(input)

    def parse(self, input) -> list:
        return [[int(n) for n in list(line.strip())] for line in input]

    def getXY(self, x, y):
        if x < 0 or y < 0:
            return 10
        if x >= len(self.table[0]) or y >= len(self.table):
            return 10
        return self.table[y][x]

    def isMin(self, x, y):
        val = self.table[y][x]
        if val >= self.getXY(x - 1, y) or val >= self.getXY(x + 1, y):
            return False
        if val >= self.getXY(x, y - 1) or val >= self.getXY(x, y + 1):
            return False
        return True

    def getMinimumsCoord(self):
        points = []
        for y in range(len(self.table)):
            for x in range(len(self.table[y])):
                if self.isMin(x, y):
                    points.append((x, y))
        return points

    def getMinimums(self):
        points = []
        for y in range(len(self.table)):
            for x in range(len(self.table[y])):
                if self.isMin(x, y):
                    points.append(self.table[y][x])
        return points

    def getEX1Result(self):
        m = self.getMinimums()
        result = sum(m) + len(m)
        print("Ex1 result", result)
        return result

    def getHigherNeighbours(self, x, y):
        points = {(x, y)}
        val = self.table[y][x]

        if val < self.getXY(x - 1, y) and self.getXY(x - 1, y) < 9:
            points.update(self.getHigherNeighbours(x - 1, y))
        if val < self.getXY(x + 1, y) and self.getXY(x + 1, y) < 9:
            points.update(self.getHigherNeighbours(x + 1, y))
        if val < self.getXY(x, y - 1) and self.getXY(x, y - 1) < 9:
            points.update(self.getHigherNeighbours(x, y - 1))
        if val < self.getXY(x, y + 1) and self.getXY(x, y + 1) < 9:
            points.update(self.getHigherNeighbours(x, y + 1))
        return points

    def getEx2Results(self):
        points = self.getMinimumsCoord()
        groups = [len(self.getHigherNeighbours(point[0], point[1])) for point in points]
        groups.sort()

        result = groups[-3] * groups[-2] * groups[-1]
        print("EX2 result", result)
        return  result


if __name__ == "__main__":
    test = Table(open("test.txt", "r").readlines())
    data = Table(open("data.txt", "r").readlines())

    assert test.getEX1Result() == 15
    assert data.getEX1Result() == 564

    assert test.getEx2Results() == 1134
    assert data.getEx2Results() == 1038240