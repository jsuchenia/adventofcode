from dataclasses import dataclass
from typing import Self, Iterable

from PIL import Image, ImageDraw, ImageFont


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


def get_map_as_str(area: dict[Point, str]) -> str:
    max_x = max(p.x for p in area.keys())
    max_y = max(p.y for p in area.keys())

    r = []
    for y in range(max_y + 1):
        r.append(''.join(map(lambda p: area[p] if p in area else ' ', [Point(x=x, y=y) for x in range(max_x + 1)])))
    return '\n'.join(r)


def get_map_as_img(area: dict[Point, str]) -> Image:
    font = ImageFont.load_default_imagefont()

    text = get_map_as_str(area)
    W, H = (10_000, 10_000)

    image = Image.new("RGBA", (W, H), "white")
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text((0, 0), text, font=font, fill="black")

    im_cropped = image.crop((0, 0, w, h))

    return im_cropped


def print_map(area: dict[Point, str]) -> None:
    print(get_map_as_str(area))


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
