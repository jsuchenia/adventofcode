import pytest

def get_data(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return [line.strip() for line in f.readlines()]

def solution1(file_name: str) -> int:
    data = get_data(file_name)
    only_digits = ["".join([char for char in line if char.isdigit()]) for line in data]
    only_two = [int(line[0] + line[-1]) for line in only_digits]
    return sum(only_two)

MAGIC_WORDS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

def convert(line: str):
    out = ""
    for idx in range(len(line)):
        if line[idx].isdigit():
            out += line[idx]
            continue

        for key, value in MAGIC_WORDS.items():
            if line[idx:].startswith(key):
                out += value
                break
    return out

def solution2(file_name: str) -> int:
    data = get_data(file_name)
    converted = [convert(line) for line in data]
    only_two = [int(line[0] + line[-1]) for line in converted]
    return sum(only_two)

@pytest.mark.parametrize("filename, result", [("test.txt", 142), ("data.txt", 54304)])
def test_part_1(filename: str, result: int):
    assert solution1(filename) == result

@pytest.mark.parametrize("filename, result", [("test2.txt", 281), ("data.txt", 54418)])
def test_part_2(filename: str, result: int):
    assert solution2(filename) == result
