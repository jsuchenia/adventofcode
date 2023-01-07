def read_data(filename: str):
    with open(filename) as f:
        return [int(line.strip()) for line in f.readlines()]

def mix(filename: str, ecnkey=1, repeats=1):
    nrs = read_data(filename)
    l = len(nrs)
    orig = [(i, val * ecnkey) for i, val in enumerate(nrs)]
    cpy = orig.copy()

    for i in range(repeats):
        # print(f" - Round {i}")
        for val in orig:
            if val[1] == 0:
                continue

            cur = cpy.index(val)
            dst = (cur + val[1]) % (l - 1)
            cpy.remove(val)
            cpy.insert(dst, val)

    final = [val for i, val in cpy]
    pos = final.index(0)

    result = final[(pos + 1000) % l], final[(pos + 2000) % l], final[(pos + 3000) % l]
    s = sum(result)
    print(f"{result=} {s=}")
    return s

def test_gps_p1_example():
    assert mix("example.txt") == 3

def test_gps_p1_data():
    assert mix("data.txt") == 8721

def test_gps_p2_example():
    assert mix("example.txt", ecnkey=811589153, repeats=10) == 1623178306

def test_gps_p1_data():
    assert mix("data.txt", ecnkey=811589153, repeats=10) == 831878881825
