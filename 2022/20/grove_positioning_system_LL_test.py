# Based on Custom LL

class N:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

def read_data(filename: str):
    with open(filename) as f:
        return [int(line.strip()) for line in f.readlines()]

def mix(filename: str, enckey=1, repeats=1):
    nrs = read_data(filename)
    l = len(nrs)

    nodes = [N(val * enckey) for val in nrs]
    for i in range(len(nodes)):
        nodes[i].next = nodes[(i + 1) % l]
        nodes[i].prev = nodes[(i - 1) % l]

    for _ in range(repeats):
        for node in nodes:
            cur = node

            if node.val == 0:
                continue
            elif node.val > 0:
                steps = node.val % (l - 1)
                for _ in range(steps):
                    cur = cur.next
            else:
                # Rewind one more to be always BEFORE insertion
                steps = -node.val % (l - 1)
                for _ in range(steps + 1):
                    cur = cur.prev

            if cur == node:
                continue

            # Cut node from old position
            node.next.prev = node.prev
            node.prev.next = node.next

            # Insert into new position (after cur)
            node.next = cur.next
            node.prev = cur

            cur.next.prev = node
            cur.next = node

    zero = [node for node in nodes if node.val == 0].pop()
    result = []

    for _ in range(3):
        for _ in range(1000 % l):
            zero = zero.next
        result.append(zero.val)

    s = sum(result)
    print(f"{result=} {s=}")
    return s

def test_gps_ll_p1_example():
    assert mix("example.txt") == 3

def test_gps_ll_p1_data():
    assert mix("data.txt") == 8721

def test_gps_ll_p2_example():
    assert mix("example.txt", enckey=811589153, repeats=10) == 1623178306

def test_gps_ll_p2_data():
    assert mix("data.txt", enckey=811589153, repeats=10) == 831878881825
