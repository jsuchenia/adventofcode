# Pulse Propagation - https://adventofcode.com/2023/day/20

from collections import defaultdict
from math import lcm
from queue import Queue

def get_data(filename: str) -> dict[str, list]:
    with open(filename) as f:
        lines = f.read().splitlines()
    lines = [line.strip().split(' -> ') for line in lines]

    modules = {}
    for name, targets in lines:
        targets = [target.strip() for target in targets.split(',')]
        if name[0] == '%':
            modules[name[1:]] = [targets, '%', False]
        elif name[0] == '&':
            modules[name[1:]] = [targets, '&', {}]
        else:
            modules[name] = [targets, 'b']
    for name, module in modules.items():
        for target in module[0]:
            if target in modules and modules[target][1] == '&':
                modules[target][2][name] = False
    return modules

def q1(filename: str, button_pushes=1000) -> int:
    modules = get_data(filename)
    low = high = 0

    for _ in range(button_pushes):
        q = Queue()
        for target in modules["broadcaster"][0]:
            q.put((target, False, "broadcaster"))
        low += 1

        while not q.empty():
            target, signal, source = q.get()
            # print(f"from: {source} to {target} - {signal}")
            if signal:
                high += 1
            else:
                low += 1

            if target not in modules:
                continue
            module = modules[target]
            module_type = module[1]

            if module_type == '%':
                if not signal:
                    module[2] = not module[2]
                    output = module[2]
                    for dst in module[0]:
                        q.put((dst, output, target))
            elif module_type == '&':
                module[2][source] = signal
                # print(f"Checking {target} - {module[2]}")
                output = False if all(val == True for val in module[2].values()) else True
                for dst in module[0]:
                    q.put((dst, output, target))
            else:
                raise ValueError("Unsupported type")

        # print(f"{high=} {low=}")

    return high * low

def q2(filename: str) -> int:
    modules = get_data(filename)
    # Rx is only in nr - but extract it from a code
    observe = [name for name, module in modules.items() if "rx" in module[0]][0]
    cycles = defaultdict(int)
    button_pushes = 0

    while True:
        button_pushes += 1
        q = Queue()
        for target in modules["broadcaster"][0]:
            q.put((target, False, "broadcaster"))

        while not q.empty():
            target, signal, source = q.get()

            # Rx is in nr, which is conjunction - so all inputs needs to be True
            # And the same situation as in day 8 - we can use lcm()
            if target == observe and signal:
                cycles[source] = button_pushes
                if len(cycles) == len(modules[observe][2]):
                    return lcm(*cycles.values())

            if target not in modules:
                continue
            module = modules[target]
            module_type = module[1]

            if module_type == '%':
                if not signal:
                    module[2] = not module[2]
                    output = module[2]
                    for dst in module[0]:
                        q.put((dst, output, target))
            elif module_type == '&':
                module[2][source] = signal
                # print(f"Checking {target} - {module[2]}")
                output = False if all(val == True for val in module[2].values()) else True
                for dst in module[0]:
                    q.put((dst, output, target))
            else:
                raise ValueError("Unsupported module type")

def test_q1():
    assert q1("test.txt", button_pushes=1) == 32
    assert q1("test2.txt", button_pushes=1) == 16
    assert q1("test.txt", button_pushes=1000) == 32_000_000
    assert q1("test2.txt", button_pushes=1000) == 11_687_500
    assert q1("data.txt", button_pushes=1000) == 814934624

def test_q2():
    assert q2("data.txt") == 228282646835717
