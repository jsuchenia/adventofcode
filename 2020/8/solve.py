#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/8
TEST_CODE = \
"""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

TEST_CODE2 = \
"""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6
"""
def calculateAccumulator(data, atLoop = True):
    acc = 0
    visited = set()
    cp = 0
    lmax = len(data)

    while True:
        if cp in visited:
            if atLoop:
                print("Acc =", acc)
                return acc
            else:
                return -1

        if cp == lmax and not atLoop:
            print("ACC at exit =", acc)
            return acc

        if cp >= lmax:
            return -1

        visited.add(cp)
        line = data[cp].strip()
        cmd = line[0:3]
        value = int(line[4:])

        if cmd == "nop":
            cp += 1
        elif cmd == "acc":
            acc += value
            cp += 1
        elif cmd == "jmp":
            cp+= value
        else:
            print("Unknown cmd", cmd, " at line", cp)
            break

    return -1

def mutationTesting(data):
    for i in range(len(data)):
        line = data[i].strip()
        if line[0:3] == "jmp":
            newData = data.copy()
            newData[i] = "nop" + data[i][3:]

            result = calculateAccumulator(newData, False)
            if result > 0:
                return result
        elif line[0:3] == "nop":
            newData = data.copy()
            newData[i] = "jmp" + data[i][3:]

            result = calculateAccumulator(newData, False)
            if result > 0:
                return result
    return -1

if __name__ == "__main__":
    testData = TEST_CODE.splitlines()
    testData2 = TEST_CODE2.splitlines()
    data = open("data", "r").read().splitlines()

    assert calculateAccumulator(testData) == 5
    calculateAccumulator(data)

    assert calculateAccumulator(testData2, False) == 8
    assert mutationTesting(testData) == 8
    assert mutationTesting(data) == 1643