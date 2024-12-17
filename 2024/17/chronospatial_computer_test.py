# Chronospatial Computer - https://adventofcode.com/2024/day/17
from functools import cache


def get_data(filename: str) -> tuple[list[int], tuple[int, ...]]:
    with open(filename) as f:
        regs, program = f.read().strip().split("\n\n")

    regs = [int(reg.split(":")[1]) for reg in regs.splitlines()]
    program = tuple(map(int, program.strip().split(":")[1].strip().split(',')))

    return regs, program


@cache
def eval_prog(program: tuple[int, ...], reg_a: int) -> tuple[int, ...]:
    regs = [reg_a, 0, 0]
    result, sp = [], 0

    def combo(operand):
        if 0 <= operand <= 3:
            return operand
        elif 4 <= operand <= 6:
            return regs[operand - 4]
        else:
            raise ValueError(f"Unknown operand {operand} at {sp=}")

    while sp < len(program):
        # print(f"{opcode=} at {sp=}")
        # print(f"{regs=}")
        match opcode := program[sp]:
            case 0:  # adv A = A // 2 ** combo
                regs[0] = regs[0] // 2 ** combo(program[sp + 1])
            case 1:  # bxl B = B ^ val
                regs[1] = regs[1] ^ program[sp + 1]
            case 2:  # bst B = combo % 8
                regs[1] = combo(program[sp + 1]) % 8
            case 3:  # jnz
                if regs[0] > 0: sp = program[sp + 1] - 2
            case 4:  # bxc B = B ^ C
                regs[1] = regs[1] ^ regs[2]
            case 5:  # out combo
                result.append(combo(program[sp + 1]) % 8)
            case 6:  # bdv B = A // 2 ** combo
                regs[1] = regs[0] // 2 ** combo(program[sp + 1])
            case 7:  # cdv C = A // 2 ** combo
                regs[2] = regs[0] // 2 ** combo(program[sp + 1])
            case _:
                raise ValueError(f"Unknown opcode {opcode} at {sp=}")
        sp += 2

    return tuple(result)


def q1(filename: str) -> str:
    regs, program = get_data(filename)
    print(f"Initial {regs=}, {program=}")

    return ','.join(str(x) for x in eval_prog(program, regs[0]))


# Test: 0,1,5,4,3,0
# A = A // 2 ** 1
# print(A % 8)
# zuruck....

# Prod: 2,4 1,3 7,5 1,5 0,3 4,3 5,5 3,0
# B = A % 8
# B = B ^ 3
# C = A // 2 ** B
# B = B ^ B
# A = A // 8
# B = B ^ C
# print B
# zuruck

def q2(filename: str) -> int:
    _, program = get_data(filename)

    def check_a(a: int) -> int:
        for i in range(8):
            if (val := eval_prog(program, a + i)) == program:
                return a + i
            elif val == program[-len(val):] and (res := check_a((a + i) << 3)) >= 0:
                return res
        return -1

    return check_a(1)


def test_q1():
    assert q1("test.txt") == '4,6,3,5,6,3,5,2,1,0'
    assert q1("data.txt") == '6,2,7,2,3,1,6,0,5'


def test_q2():
    assert q2("test2.txt") == 117440
    assert q2("data.txt") == 236548287712877
