#!/usr/local/bin/python3
def calcNextTime(timestamp, line):
    diff = timestamp % line
    if diff > 0:
        diff = line - diff
    return diff

def ex1(data):
    (timestamp, lines) = data.split("\n")
    timestamp=int(timestamp)
    lines = [int(line) for line in lines.split(",") if line != "x"]
    diff = {calcNextTime(timestamp, line):line for line in lines}

    minDiff = min(diff.keys())

    result = minDiff * diff[minDiff]
    print("Ex1 result: ", result)
    return result

def ex2(data):
    (_, lines) = data.split("\n")

    time = 1
    interval = 1
    lines = [int(x) if x != 'x' else 1 for x in lines.split(',')]

    for index, bus in enumerate(lines):
        print("Checking bus={} with index={}".format(bus, index))
        while True:
            if (time+index) % bus == 0:
                interval *= bus
                break
            time += interval

    print("Ex2 result time is", time)
    return time
if __name__ == "__main__":
    TEST_DATA="939\n7,13,x,x,59,x,31,19"
    data = open("data.txt", "r").read()

    assert ex1(TEST_DATA) == 295
    assert ex1(data) == 2382
    assert ex2(TEST_DATA) == 1068781
    assert ex2(data) == 906332393333683