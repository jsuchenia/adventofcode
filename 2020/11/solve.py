#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/11
class Layout:
    def __init__(self, input):
        self.layout = [list(line.strip()) for line in input]

    def getAdjacent(self, x, y, useVisibleAdjacent):
        adjacent = set()
        for dy in range(-1,2):
            for dx in range(-1,2):
                if dx == 0 and dy == 0:
                    continue

                nx = x
                ny = y

                while True:
                    nx += dx
                    ny += dy

                    if ny < 0 or ny >= len(self.layout):
                        break
                    if nx < 0 or nx >= len(self.layout[ny]):
                        break
                    val = self.layout[ny][nx]
                    if val == '.' and useVisibleAdjacent:
                        continue
                    adjacent.add((nx, ny))
                    break
        return adjacent

    def runRules(self, useVisibleAdjacents):
        changes = []

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                val = self.layout[y][x]
                if val == '.':
                    continue
                adjValues = [self.layout[adj[1]][adj[0]] for adj in self.getAdjacent(x, y, useVisibleAdjacents)]

                if val == 'L' and ('#' not in adjValues):
                    changes.append((x, y, '#'))
                elif val == '#' and (adjValues.count("#") >= (5 if useVisibleAdjacents else 4)):
                    changes.append((x, y, 'L'))
        for change in changes:
            self.layout[change[1]][change[0]] = change[2]
        return len(changes)

    def ex1(self):
        while self.runRules(False) > 0:
            continue

        result = sum([row.count('#') for row in self.layout])
        print("Ex1 result =", result)
        return result

    def ex2(self):
        while self.runRules(True) > 0:
            pass

        result = sum([row.count('#') for row in self.layout])
        print("Ex2 result =", result)
        return result

    def dump(self):
        for line in self.layout:
            print(''.join(line))

if __name__ == "__main__":
    testInput = open("test.txt", "r").readlines()
    input = open("data.txt", "r").readlines()

    assert Layout(testInput).ex1() == 37
    assert Layout(input).ex1() == 2303

    assert Layout(testInput).ex2() == 26
    assert Layout(input).ex2() == 2057
