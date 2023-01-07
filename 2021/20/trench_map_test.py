#!/usr/local/bin/python3

def parse(data):
    pattern, picture = data.split("\n\n")
    picture = picture.splitlines()

    return pattern, picture

def encodePicture(picture):
    return set((x, y) for y in range(len(picture)) for x in range(len(picture[y])) if picture[y][x] == '#')

def getPointValue(point, pic, borderRange, outOfBorderValue):
    x = point[0]
    y = point[1]
    (minx, maxx, miny, maxy) = borderRange

    if point in pic:
        return "1"
    elif x < minx - 3 or x > maxx + 3 or y < miny - 3 or y > maxy + 3:
        return outOfBorderValue
    else:
        return "0"

def encodePosition(point, pic, borderRange, outOfBorderValue):
    x = point[0]
    y = point[1]

    positions = [(nx, ny) for ny in range(y - 1, y + 2) for nx in range(x - 1, x + 2)]
    return int(''.join([getPointValue(p, pic, borderRange, outOfBorderValue) for p in positions]), 2)

def doEnhancement(pic, pattern, filledBorder):
    allx = [p[0] for p in pic]
    ally = [p[1] for p in pic]

    minx, maxx = min(allx), max(allx)
    miny, maxy = min(ally), max(ally)

    toEnable = set()
    toDisable = set()

    for y in range(miny - 2, maxy + 3):
        for x in range(minx - 2, maxx + 3):
            point = (x, y)
            pos = encodePosition(point, pic, (minx, maxx, miny, maxy), "0" if filledBorder else "1")
            if pattern[pos] == '#' and point not in pic:
                toEnable.add(point)
            elif pattern[pos] == '.' and point in pic:
                toDisable.add(point)

    pic.difference_update(toDisable)
    pic.update(toEnable)

def ex1(filename, rounds):
    data = open(filename, "r").read()
    pattern, picture = parse(data)
    encpic = encodePicture(picture)

    for _ in range(rounds):
        filledBorder = True if pattern[0] == '#' else False
        doEnhancement(encpic, pattern, filledBorder)

    solution = len(encpic)
    print(f"{solution=}")
    return solution

def test_scan_ex1_test():
    assert ex1("test.txt", rounds=2) == 35

def test_scan_ex1_data():
    assert ex1("data.txt", rounds=2) == 6262

def test_scan_ex2_test():
    assert ex1("test.txt", rounds=50) == 3351

def test_scan_ex2_data():
    assert ex1("data.txt", rounds=50) == 49765
