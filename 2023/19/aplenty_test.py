# Aplenty - https://adventofcode.com/2023/day/19
from math import prod

def get_data(filename: str) -> tuple[dict, list]:
    with open(filename) as f:
        rules, values = f.read().strip().split('\n\n')

    workflows = {}
    for rule in rules.split('\n'):
        sep = rule.index('{')
        name, value = rule[:sep], rule[sep + 1:-1]
        workflows[name] = value.split(',')
    values = [value[1:-1].split(',') for value in values.split('\n')]
    values = [{e.split('=')[0]: int(e.split('=')[1]) for e in value} for value in values]
    return workflows, values

def q1(filename: str) -> int:
    workflows, parts = get_data(filename)

    def eval_rule(values: dict[str, int], rule: str) -> bool:
        if rule == "R":
            return False
        elif rule == "A":
            return True

        for statement in workflows[rule]:
            if ':' in statement:
                check, new_rule = statement.split(':')
                variable, op, value = check[0], check[1], int(check[2:])

                if op == '<' and values[variable] < value:
                    return eval_rule(values, new_rule)
                elif op == '>' and values[variable] > value:
                    return eval_rule(values, new_rule)
            else:
                return eval_rule(values, statement)

    return sum(sum(part.values()) for part in parts if eval_rule(part, 'in'))

def q2(filename: str) -> int:
    workflows, _ = get_data(filename)

    def count_ranges(ranges, rule: str) -> int:
        if rule == "R":
            return 0
        elif rule == "A":
            return prod(stop - start + 1 for start, stop in ranges.values())

        result = 0
        for statement in workflows[rule]:
            if ':' in statement:
                check, new_rule = statement.split(':')
                variable, op, value = check[0], check[1], int(check[2:])
                start, stop = ranges[variable]

                if op == '<':
                    new_range = (start, min(value - 1, stop))
                    out_of_range = (max(value, start), stop)
                elif op == '>':
                    out_of_range = (start, min(value, stop))
                    new_range = (max(value + 1, start), stop)
                else:
                    raise ValueError(f"Unknown operation {op=}")

                if new_range[0] <= new_range[1]:
                    result += count_ranges({**ranges, variable: new_range}, new_rule)

                if out_of_range[0] <= out_of_range[1]:
                    ranges[variable] = out_of_range
                else:
                    return result
            else:
                result += count_ranges(ranges, statement)
        return result

    return count_ranges({key: (1, 4000) for key in "xmas"}, "in")

def test_q1():
    assert q1("test.txt") == 19114
    assert q1("data.txt") == 342650

def test_q2_custom():
    assert q2("test_q2.txt") == 1
    assert q2("test_q2_2.txt") == 4
    assert q2("test_q2_3.txt") == 0

def test_q2():
    assert q2("test.txt") == 167409079868000
    assert q2("data.txt") == 130303473508222
