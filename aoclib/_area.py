from dataclasses import dataclass
from typing import Self


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


N = Point(x=0, y=1)
S = Point(x=0, y=-1)
E = Point(x=1, y=0)
W = Point(x=-1, y=0)

DIRECTIONS_4 = (N, E, S, W)

NE = N + E
SE = S + E
SW = S + W
NW = N + W

DIRECTIONS_8 = (N, NE, E, SE, S, SW, W, NW)
