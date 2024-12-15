from tqdm import tqdm

from aoclib import *
from warehouse_woes_test import MOVES, get_data, resize_map


def simulate(filename: str, resize, image_name: str, ratio=1) -> None:
    area, start, moves = get_data(filename)
    if resize:
        area, start = resize_map(area), Point(x=2 * start.x, y=start.y)

    total = len(moves)
    images = [get_map_as_img(area, footer=f"0/{total}")]

    for idx, move in enumerate(tqdm(moves, desc=image_name)):
        positions = [start]
        to_move = [start]
        direction = MOVES[move]

        while True:
            next_positions = []
            for point in positions:
                point = point + direction
                val = area[point]
                if val == '[':
                    next_positions.append(point)
                    if direction in (S, N):
                        next_positions.append(point + E)
                elif val == ']':
                    next_positions.append(point)
                    if direction in (S, N):
                        next_positions.append(point + W)
                elif val == 'O':
                    next_positions.append(point)
                elif val == '.':
                    continue
                elif val == '#':
                    to_move.clear()
                    break
                else:
                    raise ValueError(f"Wrong value of point {point=} {val=}")

            if next_positions and to_move:
                to_move.extend(next_positions)
                positions = next_positions
                continue
            else:
                break

        if to_move:
            for point in reversed(list(dict.fromkeys(to_move))):  # Unique elements in a reverse order
                area[point + direction], area[point] = area[point], area[point + direction]

            start = start + direction

        if (idx % ratio) == 0:
            images.append(get_map_as_img(area, footer=f"{idx}/{total}"))

    first = images[0]
    other = images[1:]
    print(f"Saving {len(images)=}")
    first.save(image_name, save_all=True, append_images=other, duration=60, loop=0)


if __name__ == "__main__":
    simulate("test1.txt", False, "animation-part1-test1.gif")
    simulate("test2.txt", False, "animation-part1-test2.gif", ratio=10)
    simulate("data.txt", False, "animation-part1-data.gif", ratio=100)

    simulate("test3.txt", True, "animation-part2-test3.gif")
    simulate("test2.txt", True, "animation-part2-test2.gif", ratio=10)
    simulate("data.txt", True, "animation-part2-data.gif", ratio=100)
