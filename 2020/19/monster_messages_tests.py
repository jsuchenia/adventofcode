#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/19

REPLACEMENT = "8: 42 |42 8\n11: 42 31 | 42 11 31"

def parseRules(data):
    rules = {}

    for line in data.splitlines():
        id, syntax = line.strip().split(":")
        syntax = syntax.strip()

        if syntax[0] == '"':
            rules[int(id)] = syntax[1]
        else:
            if '|' in syntax:
                res = set(tuple(int(i) for i in r.strip().split(" ")) for r in syntax.split("|"))
            else:
                res = tuple(int(i) for i in syntax.strip().split(" "))
            rules[int(id)] = res

    return rules

def checkRule(rules, rule, posList, line, incr=0):
    ruletype = type(rule)

    if len(posList) == 0:
        return []

    # Rule can evaluate "true" after different pos - especially or syntax
    result = []

    if ruletype is str:
        result.extend([pos + 1 for pos in posList if pos < len(line) and line[pos] == rule])
    elif ruletype is set:
        for subrule in rule:
            result.extend(checkRule(rules, subrule, posList, line, incr + 1))
    elif ruletype is tuple:
        curpos = posList
        for ruleId in rule:
            npos = checkRule(rules, rules[ruleId], curpos, line, incr + 1)
            curpos = npos
            if len(curpos) == 0:
                break

        if len(curpos) > 0:
            result.extend(curpos)
    return result

def checkEntry(rules, line):
    last_pos = checkRule(rules, rules[0], [0], line.strip())
    if len(line) in last_pos:
        return True

    return False

def evaluate_messages(data, replace=False):
    rdata, entries = data.split("\n\n")
    rules = parseRules(rdata)
    if replace:
        rules.update(parseRules(REPLACEMENT))

    result = 0
    for line in entries.splitlines():
        if checkEntry(rules, line):
            result += 1

    print("Ex1", result)
    return result

def test_messages_test1():
    test = open("test.txt", "r").read()
    assert evaluate_messages(test) == 2

def test_messages_test2():
    test2 = open("test2.txt", "r").read()
    assert evaluate_messages(test2) == 3

def test_messages():
    data = open("data.txt", "r").read()
    assert evaluate_messages(data) == 124

def test_messages_with_replacement_test1():
    test = open("test.txt", "r").read()
    assert evaluate_messages(test, replace=True) == 2

def test_messages_with_replacement_test2():
    test2 = open("test2.txt", "r").read()
    assert evaluate_messages(test2, replace=True) == 12

def test_messages_with_replacement_test3():
    test3 = open("test3.txt", "r").read()
    assert evaluate_messages(test3, replace=True) == 1

def test_messages_with_replacement():
    data = open("data.txt", "r").read()
    assert evaluate_messages(data, replace=True) == 228
