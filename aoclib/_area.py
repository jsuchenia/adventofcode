from typing import Iterable

from PIL import ImageFont, Image, ImageDraw


def parse_map(lines: Iterable[Iterable[str]]) -> dict[complex, str]:
    result = dict()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            result[y + 1j * x] = ch
    return result


# In our examples (where top,left corner is 0,0) this is how we map N,S,E,W
N = -1
S = 1
E = 1j
W = -1j

DIRECTIONS_4 = (N, E, S, W)

NE = N + E
SE = S + E
SW = S + W
NW = N + W

DIRECTIONS_8 = (N, NE, E, SE, S, SW, W, NW)


# Visualization of an area - str, ASCII and PIL Image
def get_map_as_str(area: dict[complex, str]) -> str:
    max_x = max(p.imag for p in area.keys())
    max_y = max(p.real for p in area.keys())

    r = []
    for y in range(max_y + 1):
        r.append(''.join(map(lambda p: area[p] if p in area else ' ', [y + 1j * x for x in range(max_x + 1)])))
    return '\n'.join(r)


def get_map_as_img(area: dict[complex, str], *, footer: str = "") -> Image:
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


def print_map(area: dict[complex, str]) -> None:
    print(get_map_as_str(area))
