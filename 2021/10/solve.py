#!/usr/local/bin/python3
# https://adventofcode.com/2021/day/10
VALID_STARTS = {'(':  1, '[': 2, '{':  3, '<': 4}
VALID_ENDS = {'}': ('{', 1197), ')': ('(', 3), ']': ('[', 57), '>': ('<', 25137)}

def countErrors(line, scoreEnding):
    elements = list(line)
    stack = []

    for e in elements:
        if e in VALID_STARTS:
            stack.append(e)
        elif e in VALID_ENDS:
            matchingStart = VALID_ENDS[e][0]

            if len(stack) > 0 and stack[-1] == matchingStart:
                del stack[-1]
            else:
                if not scoreEnding:
                    print("Wrong char ", e, " cost ", VALID_ENDS[e][1])
                    return VALID_ENDS[e][1]
                else:
                    return 0

    if scoreEnding:
        total = 0
        for score in [VALID_STARTS[e] for e in stack[::-1]]:
            total *= 5
            total += score
        print("Invalid line, score", total)
        return total
    else:
        return 0

def ex2(lines):
    results = sorted([countErrors(line, scoreEnding=True) for line in lines])
    results = [result for result in results if result > 0]
    print("Sorted results", results)
    result = results[len(results) // 2]

    print("Ex2: ", result)
    return result

def ex1(lines):
    result = sum([countErrors(line, scoreEnding=False) for line in lines])

    print("Ex1: ", result)
    return result

if __name__ == "__main__":
    testData = [line.strip() for line in open("test.txt", "r").readlines()]
    data = [line.strip() for line in open("data.txt", "r").readlines()]

    assert ex1(testData) == 26397
    assert ex1(data) == 167379

    assert ex2(testData) == 288957
    assert ex2(data) == 2776842859
