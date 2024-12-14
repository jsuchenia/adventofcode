from re import findall


def ints(line: str) -> tuple[int, ...]:
    return tuple(map(int, findall(r'(-?\d+)', line)))
