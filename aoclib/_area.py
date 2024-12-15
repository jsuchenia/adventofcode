from dataclasses import dataclass
from typing import Self, Iterable

from PIL import ImageFont, Image, ImageDraw


@dataclass(kw_only=True, frozen=True)
class AoCPoint:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return AoCPoint(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return AoCPoint(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: int) -> Self:
        return AoCPoint(x=self.x * other, y=self.y * other)

    def __rmul__(self, other: int) -> Self:
        return AoCPoint(x=self.x * other, y=self.y * other)


def parse_map(lines: Iterable[Iterable[str]]) -> dict[AoCPoint, str]:
    result = dict()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            result[AoCPoint(x=x, y=y)] = ch
    return result


# In our examples (where top,left corner is 0,0) this is how we map N,S,E,W
N = AoCPoint(x=0, y=-1)
S = AoCPoint(x=0, y=1)
E = AoCPoint(x=1, y=0)
W = AoCPoint(x=-1, y=0)

DIRECTIONS_4 = (N, E, S, W)

NE = N + E
SE = S + E
SW = S + W
NW = N + W

DIRECTIONS_8 = (N, NE, E, SE, S, SW, W, NW)


# Visualization of an area - str, ASCII and PIL Image
def get_map_as_str(area: dict[AoCPoint, str]) -> str:
    max_x = max(p.x for p in area.keys())
    max_y = max(p.y for p in area.keys())

    r = []
    for y in range(max_y + 1):
        r.append(''.join(map(lambda p: area[p] if p in area else ' ', [AoCPoint(x=x, y=y) for x in range(max_x + 1)])))
    return '\n'.join(r)


def get_map_as_img(area: dict[AoCPoint, str], *, footer: str = "") -> Image:
    font = ImageFont.load_default_imagefont()

    text = get_map_as_str(area)
    if footer:
        text += "\n\n"
        text += footer
    W, H = (10_000, 10_000)

    image = Image.new("RGBA", (W, H), "white")
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text((0, 0), text, font=font, fill="black")

    im_cropped = image.crop((0, 0, w, h))

    return im_cropped


def print_map(area: dict[AoCPoint, str]) -> None:
    print(get_map_as_str(area))
