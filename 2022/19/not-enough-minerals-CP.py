import re

from cpmpy import intvar, Model, cpm_array


# CP - Constrain programming - https://cpmpy.readthedocs.io/
# Based on: https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0ty6zr/?utm_source=share&utm_medium=web2x&context=3
#     Code: https://pastebin.com/w2brfTme

def read_data(filename: str):
    pattern = re.compile(f"\d+")
    with open(filename) as f:
        return [list(map(int, pattern.findall(line))) for line in f.readlines()]


# DFS like - go deep and check how much goede we earn
def simul(id, ore_cost_ore, clay_cost_ore, obs_cost_ore, obs_cost_clay, geode_cost_ore, geode_cost_obs, limit):
    # Cost of each decision - each row is a decision, each colum is a cost of it
    # 0 - is just wait, 1 - buy ORE harvester, 2 - buy CLAY harvester, 3 - buy obsidian harvester, 4 - buy geode harvester
    cost_array = cpm_array([
        [0, 0, 0, 0],
        [ore_cost_ore, 0, 0, 0],
        [clay_cost_ore, 0, 0, 0],
        [obs_cost_ore, obs_cost_clay, 0, 0],
        [geode_cost_ore, 0, geode_cost_obs, 0],
    ])
    decision = intvar(0, 4, shape=(limit + 1, 1), name="decision")

    # Number of bots that we have "active" AT the end current round
    bots = intvar(0, 100, shape=(limit + 1, 4), name="bots")
    # Resources that we have in each round
    resources = intvar(0, 500, shape=(limit + 1, 4), name="resources")

    model = Model()

    # Initial values for step 0 - only 1 ORE harvester and 0 resources
    model += bots[0] == (1, 0, 0, 0)
    model += resources[0] == (0, 0, 0, 0)

    for res_id in range(4):
        for step in range(1, limit + 1):
            what_to_buy = decision[step, 0]

            # To buy a harvester we need to have enough resources
            model += resources[step - 1, res_id] >= cost_array[what_to_buy, res_id]

            # This is how we calculate resources at the end of this round
            resource_cost_in_step = cost_array[what_to_buy, res_id]
            model += resources[step, res_id] == resources[step - 1, res_id] + bots[step - 1, res_id] - resource_cost_in_step

            # Number of bots will be increased by a decision
            # In CPMpy we have to convert if statements to math calculation
            extra_bot_for_resource = (what_to_buy - 1) == res_id
            model += bots[step, res_id] == bots[step - 1, res_id] + extra_bot_for_resource

    model.maximize(resources[limit, 3])  # Objective: maximize the number of geodes in the end

    if model.solve():
        print(f"  [{id}] {model.status()}")
        return resources[limit, 3].value()
    raise ValueError("No solution for this clue!")


def do_simulationp1(filename, limit) -> int:
    blueprints = read_data(filename)
    result = 0

    for b in blueprints:
        r = simul(*b, limit=limit)
        result += r * b[0]

    print(f"P1: Multiplication result: {result}")
    return result


def do_simulationp2(filename, limit) -> int:
    blueprints = read_data(filename)
    result = 1

    for b in blueprints[:3]:
        r = simul(*b, limit=limit)
        result *= r

    print(f"P2: Multiplication result: {result}")
    return result


if __name__ == "__main__":
    data = read_data("data.txt")

    assert do_simulationp1("example.txt", limit=24) == 33
    assert do_simulationp1("data.txt", limit=24) == 1144
    assert do_simulationp2("example.txt", limit=32) == 3472
    assert do_simulationp2("data.txt", limit=32) == 19980
