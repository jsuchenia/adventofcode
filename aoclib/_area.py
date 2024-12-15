from dataclasses import dataclass
from typing import Self, Iterable


@dataclass(kw_only=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: int) -> Self:
        return Point(x=self.x * other, y=self.y * other)

    def __rmul__(self, other: int) -> Self:
        return Point(x=self.x * other, y=self.y * other)


def parse_map(lines: Iterable[Iterable[str]]) -> dict[Point, str]:
    result = dict()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            result[Point(x=x, y=y)] = ch
    return result


def print_map(area: dict[Point, str]) -> None:
    max_x = max(p.x for p in area.keys())
    max_y = max(p.y for p in area.keys())

    for y in range(max_y + 1):
        print(''.join(map(lambda p: area[p] if p in area else ' ', [Point(x=x, y=y) for x in range(max_x + 1)])))


# In our examples (where top,left corner is 0,0) this is how we map N,S,E,W
N = Point(x=0, y=-1)
S = Point(x=0, y=1)
E = Point(x=1, y=0)
W = Point(x=-1, y=0)

DIRECTIONS_4 = (N, E, S, W)

NE = N + E
SE = S + E
SW = S + W
NW = N + W

DIRECTIONS_8 = (N, NE, E, SE, S, SW, W, NW)
