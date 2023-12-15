# https://adventofcode.com/2023/day/5
import re

type Rule = list[int]
type Block = list[Rule]
type Seeds = list[tuple[int, int]]

def get_data(filename: str) -> tuple[Seeds, list[Block]]:
    with open(filename, "r") as f:
        data = f.read()

    blocks = data.split("\n\n")

    seeds = [int(n) for n in re.findall(r"(\d+)", blocks[0])]
    mapping = []
    for block in blocks[1:]:
        lines = block.splitlines()
        block_mapping = []
        for b in lines[1:]:
            block_mapping.append([int(n) for n in b.split()])
        mapping.append(block_mapping)
    return seeds, mapping

def process_mapping(seeds: Seeds, mapping: Block) -> Seeds:
    result = []

    while seeds:
        start, stop = seeds.pop()
        for dst, src, length in mapping:
            # Find overlap with a range (cheers 2022/4)
            new_start = max(start, src)
            new_stop = min(stop, src + length)

            if new_start < new_stop:
                result.append((new_start - src + dst, new_stop - src + dst))

                # !@##$#$ - We need to process what left!
                if new_start > start:
                    seeds.append((start, new_start))
                if stop > new_stop:
                    seeds.append((new_stop, stop))

                break
        else:  # Cheers to JLucka - simplified after her comment
            result.append((start, stop))

    return result

def q1(filename: str) -> int:
    input_seeds, mappings = get_data(filename)

    seeds = [(s, s + 1) for s in input_seeds]
    for mapping in mappings:
        seeds = process_mapping(seeds, mapping)

    return min([s[0] for s in seeds])

def q2(filename: str) -> int:
    input_seeds, mappings = get_data(filename)

    seeds = [(input_seeds[idx], input_seeds[idx] + input_seeds[idx + 1]) for idx in range(0, len(input_seeds), 2)]

    for mapping in mappings:
        seeds = process_mapping(seeds, mapping)

    return min([s[0] for s in seeds])

def test_q1():
    assert q1("test.txt") == 35
    assert q1("data.txt") == 993500720

def test_q2():
    assert q2("test.txt") == 46
    assert q2("data.txt") == 4917124
