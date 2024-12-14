# Post-factum script for a visualisation

import matplotlib.pyplot as plt

from restroom_redoubt_test import get_data, calc_safety_factor

X = 101
Y = 103

if __name__ == "__main__":
    robots = get_data("data.txt")
    total = len(robots)

    xval = []
    safety_scores = []
    area_size = []

    for tick in range(1, 10_000):
        area = set()
        for idx, robot in enumerate(robots):
            x, y, dx, dy = robot
            x, y = (x + dx) % X, (y + dy) % Y
            robots[idx] = (x, y, dx, dy)
            area.add((x, y))

        safety = calc_safety_factor(robots, X, Y)
        xval.append(tick)
        safety_scores.append(safety)
        area_size.append(len(area))

    plt.xscale('linear')
    plt.yscale('linear')
    plt.title("Safety score")  # This needs to be minimum
    plt.plot(xval, safety_scores)
    plt.savefig("safety_score.png")

    plt.clf()
    plt.title("Number of bots")  # This needs to be equal to bots (500)
    plt.plot(xval, area_size)
    plt.savefig("bots.png")
