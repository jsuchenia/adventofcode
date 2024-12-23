import re

from shapely import Polygon, LinearRing, unary_union, clip_by_rect


def read_data(filename: str):
    pattern = re.compile(r"=(-?\d+)")
    with open(filename) as f:
        return [map(int, pattern.findall(line)) for line in f.readlines()]


def q2(filename: str, max_range: int) -> int:
    data = read_data("data.txt")
    polygons = []

    for sx, sy, bx, by in data:
        md = abs(sx - bx) + abs(sy - by)
        polygon = Polygon([(sx, sy + md), (sx - md, sy), (sx, sy - md), (sx + md, sy)])
        assert polygon.boundary.is_ring
        polygons.append(polygon)

    union = unary_union(polygons)
    area = clip_by_rect(union, 0, 0, max_range, max_range)

    # Only one, non-covered area after clip
    assert len(area.interiors) == 1
    interior: LinearRing = area.interiors[0]

    # X,Y will be in a center of it
    assert len(interior.centroid.coords) == 1

    x, y = map(int, list(interior.centroid.coords)[0])

    return x * max_range + y


def test_q2():
    assert q2("data.txt", 4_000_000) == 10693731308112
