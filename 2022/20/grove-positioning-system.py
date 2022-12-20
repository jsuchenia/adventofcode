from collections import deque


def read_data(filename: str):
    with open(filename) as f:
        return [int(line.strip()) for line in f.readlines()]


def mix(filename: str, ecnkey=1, repeats=1):
    nrs = read_data(filename)
    l = len(nrs)
    orig = [(i, val * ecnkey) for i, val in enumerate(nrs)]
    cpy = deque(orig)

    for i in range(repeats):
        print(f" - Round {i}")
        for val in orig:
            if val[1] == 0:
                continue

            cur = cpy.index(val)
            assert cur >= 0

            dst = cur + val[1]
            while dst <= 0:
                dst += l - 1
            while dst > l:
                dst %= (l - 1)

            cpy.remove(val)
            cpy.insert(dst, val)

    final = [val for i, val in cpy]
    pos = final.index(0)

    result = final[(pos + 1000) % l], final[(pos + 2000) % l], final[(pos + 3000) % l]
    s = sum(result)
    print(f"{result=} {s=}")
    return s


if __name__ == "__main__":
    assert mix("example.txt") == 3
    assert mix("data.txt") == 8721

    assert mix("example.txt", ecnkey=811589153, repeats=10) == 1623178306
    # assert mix("data.txt", ecnkey=811589153, repeats=10) == 831878881825
