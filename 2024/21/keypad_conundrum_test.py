# Keypad Conundrum - https://adventofcode.com/2024/day/21
from functools import cache
from itertools import product

from networkx import DiGraph, all_shortest_paths

from aoclib import *


def get_data(filename: str) -> list[str]:
    with open(filename) as f:
        codes = f.read().strip().splitlines()
    return codes


num_pad = [
    "789",
    "456",
    "123",
    "#0A"
]
dir_pad = [
    "#^A",
    "<v>"
]


def build_grid(pad: list[str]) -> DiGraph:
    g = DiGraph()
    area = parse_map(pad, skip_chars="#")

    for point, val in area.items():
        for direction, move in (N, "^"), (S, "v"), (E, ">"), (W, "<"):
            next_point = point + direction
            if next_point in area:
                g.add_edge(val, area[next_point], move=move)
    return g


num_graph = build_grid(num_pad)
dir_graph = build_grid(dir_pad)


def all_moves(graph: DiGraph, btn_src: str, btn_dst: str, ) -> list[str]:
    for path in all_shortest_paths(graph, btn_src, btn_dst):
        yield ''.join([str(graph[btn_a][btn_b]["move"]) for btn_a, btn_b in zip(path, path[1:])]) + "A"


@cache
def min_dir_moves_length(code: str, num_of_dir_pads: int) -> int:
    results = 0
    for src, dst in zip("A" + code, code):
        if num_of_dir_pads > 0:
            results += min(min_dir_moves_length(moves, num_of_dir_pads - 1) for moves in all_moves(dir_graph, src, dst))
        else:
            results += min(len(moves) for moves in all_moves(dir_graph, src, dst))
    return results


def all_num_moves(code: str) -> list[str]:
    dir_input = [all_moves(num_graph, src, dst) for src, dst in zip("A" + code, code)]
    return [''.join(s) for s in product(*dir_input)]


def q1(filename: str, num_of_dir_pads) -> int:
    result = 0

    for code in get_data(filename):
        min_length = min(min_dir_moves_length(num_moves, num_of_dir_pads - 1) for num_moves in all_num_moves(code))
        result += min_length * int(code[:-1])

    return result


def test_q1():
    assert q1("test.txt", 2) == 126384
    assert q1("data.txt", 2) == 137870


def test_q2():
    assert q1("test.txt", 25) == 154115708116294
    assert q1("data.txt", 25) == 170279148659464
