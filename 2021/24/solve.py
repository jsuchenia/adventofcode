#!/usr/local/bin/python3
INDENT = "    "

from functools import cache
import sys

# RANGE_PARAMS="9,0, -1"
RANGE_PARAMS="1,10"

def parsedata(data):
    blocks = []
    start = 0
    while (end:=data.find("inp ", start+1)) >= 0:
        blocks.append(data[start:end-1])
        start = end
    blocks.append(data[start:])

    return blocks

def blocks2py(blocks):
    out = []

    for i, block in enumerate(blocks):
        lines = block.splitlines()

        out.append("\n@cache\ndef block{}(w, z):".format(i))
        assert lines[0] == "inp w"
        assert lines[1] == "mul x 0"

        if i < 3:
            out.append(f"{INDENT}print('block{i}', w, z)")
        for line in lines[1:]:
            l = line.split(" ")
            if l[0] == "add":
                out.append(INDENT + "{} += {}".format(l[1], l[2]))
            elif l[0] == "mul":
                if l[2] == "0":
                    out.append(INDENT + "{} = 0".format(l[1]))
                else:
                    out.append(INDENT + "{} *= {}".format(l[1], l[2]))
            elif l[0] == "mod":
                out.append(INDENT + "{} %= {}".format(l[1], l[2]))
            elif l[0] == "div":
                out.append(INDENT + "{} //= {}".format(l[1], l[2]))
            elif l[0] == "eql":
                out.append(INDENT + "{} = 1 if {} == {} else 0".format(l[1], l[1], l[2]))
            else:
                assert False

        if i == 13:
            out.append(f"{INDENT}if z == 0:\n{INDENT}{INDENT}print('OKOKOKOK!')\n{INDENT}{INDENT}return ' - OK'\n{INDENT}else:\n{INDENT}{INDENT}return None")
        else:
            out.append(f"{INDENT}for nw in range({RANGE_PARAMS}):\n{INDENT}{INDENT}if res:=block{i+1}(nw,z):\n{INDENT}{INDENT}{INDENT}return str(nw) + res")

    out.append(f"\n\nfor nw in range({RANGE_PARAMS}):\n{INDENT}res=block0(nw,0)\n{INDENT}if res:\n{INDENT}{INDENT}print(str(nw) + res)\n{INDENT}{INDENT}break")
    return '\n'.join(out)
if __name__ == "__main__":
    data = open("data.txt", "r").read()
    blocks = parsedata(data)
    code = blocks2py(blocks)
    print(code)
    exec(code)
    sys.exit(-1)
