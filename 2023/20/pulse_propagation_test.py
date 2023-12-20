# Pulse Propagation - https://adventofcode.com/2023/day/20

from collections import defaultdict, deque
from dataclasses import dataclass
from math import lcm

import matplotlib.pyplot as plt
import pytest
from networkx import DiGraph, draw_planar

@dataclass(kw_only=True)
class Module:
    targets: list[str]

@dataclass(kw_only=True)
class FlipFlop(Module):
    status: bool

@dataclass(kw_only=True)
class Conjunction(Module):
    last_signal: dict[str]

def get_data(filename: str) -> dict[str, Module]:
    with open(filename) as f:
        lines = f.read().splitlines()
    lines = [line.strip().split(' -> ') for line in lines]

    modules = {}
    for name, targets in lines:
        targets = [target.strip() for target in targets.split(',')]
        if name[0] == '%':
            modules[name[1:]] = FlipFlop(targets=targets, status=False)
        elif name[0] == '&':
            modules[name[1:]] = Conjunction(targets=targets, last_signal=dict[str]())
        else:
            modules[name] = Module(targets=targets)

    for name, module in modules.items():
        for target in module.targets:
            if target in modules and isinstance(modules[target], Conjunction):
                modules[target].last_signal[name] = False
    return modules

def q1(filename: str, button_pushes=1000) -> int:
    modules = get_data(filename)
    low = high = 0

    for _ in range(button_pushes):
        q = deque((target, False, "broadcaster") for target in modules["broadcaster"].targets)
        low += 1

        while q:
            target, signal, source = q.popleft()
            high += signal
            low += not signal

            module = modules.get(target, Module(targets=[]))

            if isinstance(module, FlipFlop):
                if not signal:
                    module.status = not module.status
                    for dst in module.targets:
                        q.append((dst, module.status, target))
            elif isinstance(module, Conjunction):
                module.last_signal[source] = signal
                output = not all(module.last_signal.values())

                for dst in module.targets:
                    q.append((dst, output, target))

    return high * low

def q2(filename: str) -> int:
    modules = get_data(filename)
    # Rx is only in nr - but extract it from a code
    observe = [name for name, module in modules.items() if "rx" in module.targets][0]
    cycles = defaultdict(int)
    button_pushes = 0

    while True:
        button_pushes += 1
        q = deque((target, False, "broadcaster") for target in modules["broadcaster"].targets)

        while q:
            target, signal, source = q.popleft()
            module = modules.get(target, Module(targets=[]))

            # Rx is in only nr, which is conjunction - so all inputs needs to be True
            # And the same situation as in day 8 - we can use lcm()
            if target == observe and signal and isinstance(module, Conjunction):
                cycles[source] = button_pushes
                if len(cycles) == len(module.last_signal):
                    # Hello day 8 - long time no see
                    return lcm(*cycles.values())

            if isinstance(module, FlipFlop):
                if not signal:
                    module.status = not module.status
                    for dst in module.targets:
                        q.append((dst, module.status, target))
            elif isinstance(module, Conjunction):
                module.last_signal[source] = signal
                output = not all(module.last_signal.values())
                for dst in module.targets:
                    q.append((dst, output, target))

def test_q1():
    assert q1("test.txt", button_pushes=1) == 32
    assert q1("test2.txt", button_pushes=1) == 16
    assert q1("test.txt", button_pushes=1000) == 32_000_000
    assert q1("test2.txt", button_pushes=1000) == 11_687_500
    assert q1("data.txt", button_pushes=1000) == 814934624

def test_q2():
    assert q2("data.txt") == 228282646835717

@pytest.mark.skip
def test_visualise_input():
    modules = get_data("data.txt")
    g = DiGraph()
    for name, module in modules.items():
        for target in module.targets:
            g.add_edge(name, target)
    print("Drawing...")
    draw_planar(g, with_labels=True)
    plt.savefig('data.png')
