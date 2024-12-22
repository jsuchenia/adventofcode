# Post-factum script for a visualisation
import cv2
import numpy as np
from tqdm import tqdm

from aoclib import *
from restroom_redoubt_test import get_data

X = 101
Y = 103

if __name__ == "__main__":
    robots = get_data("data.txt")
    total = len(robots)
    for tick in tqdm(range(1, 10_000)):
        area = {}
        for idx, robot in enumerate(robots):
            x, y, dx, dy = robot
            x, y = (x + dx) % X, (y + dy) % Y
            robots[idx] = (x, y, dx, dy)
            area[y + x * 1j] = '#'

        img = get_map_as_img(area, footer=f"{tick}/10.000")
        opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cv2.imshow("Visualization", opencvImage)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
