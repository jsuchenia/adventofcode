import re
from collections import deque

import pytest

def read_data(filename: str):
    pattern = re.compile(r"\d+")
    with open(filename) as f:
        return [list(map(int, pattern.findall(line))) for line in f.readlines()]

# DFS like - go deep and check how much goede we earn
def simul(id, ore_cost_ore, clay_cost_ore, obs_cost_ore, obs_cost_clay, geode_cost_ore, geode_cost_obs, limit):
    q = deque()
    q.append((0, 0, 0, 0, 1, 0, 0, 0, limit))

    i = 0
    result = 0
    seen = set()
    ore_max = max(ore_cost_ore, clay_cost_ore, obs_cost_ore, geode_cost_ore)

    while q:
        state = q.popleft()
        if state in seen:
            continue
        seen.add(state)

        ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode, t = state
        if t == 0:
            result = max(result, geode)
            continue

        # i += 1
        # if i % 1_000_000 == 0:
        #     print(f"{id=} Queue length: {len(q)}")
        #     print(f"    Status [t={limit - t}]: {ore=} {clay=} {obs=} {geode=}")
        #     print(f"    Robots [t={limit - t}]: {r_ore=} {r_clay=} {r_obs=} {r_geode=}")

        c = []
        nt = t - 1
        if ore >= geode_cost_ore and obs >= geode_cost_obs:
            c.append(
                (
                    (ore + r_ore - geode_cost_ore),
                    (clay + r_clay),
                    (obs + r_obs - geode_cost_obs),
                    (geode + r_geode),
                    r_ore,
                    r_clay,
                    r_obs,
                    r_geode + 1,
                    nt,
                )
            )

        if ore >= obs_cost_ore and clay >= obs_cost_clay and r_obs < geode_cost_obs:
            c.append((ore + r_ore - obs_cost_ore, clay + r_clay - obs_cost_clay, obs + r_obs, geode + r_geode, r_ore, r_clay, r_obs + 1, r_geode, nt))

        if ore >= clay_cost_ore and r_clay < obs_cost_clay:
            c.append(((ore + r_ore - clay_cost_ore), (clay + r_clay), (obs + r_obs), (geode + r_geode), r_ore, r_clay + 1, r_obs, r_geode, nt))

        if ore >= ore_cost_ore and r_ore < ore_max:
            c.append(((ore + r_ore - ore_cost_ore), (clay + r_clay), (obs + r_obs), (geode + r_geode), r_ore + 1, r_clay, r_obs, r_geode, nt))

        c.append((ore + r_ore, clay + r_clay, obs + r_obs, geode + r_geode, r_ore, r_clay, r_obs, r_geode, nt))

        # Cap values that we will never spend - to find out similarities
        for nore, nclay, nobs, ngeode, nr_ore, nr_clay, nr_obs, nr_geod, nt in c:
            nore = min(nore, nt * ore_max - (nt - 1) * nr_ore)
            nclay = min(nclay, nt * obs_cost_clay - (nt - 1) * nr_clay)
            nobs = min(nobs, nt * geode_cost_obs - (nt - 1) * nr_obs)

            new_state = (nore, nclay, nobs, ngeode, nr_ore, nr_clay, nr_obs, nr_geod, nt)
            if new_state not in seen:
                q.append(new_state)

    return result

def do_simulationp1(filename, limit) -> int:
    blueprints = read_data(filename)
    result = 0

    for b in blueprints:
        r = simul(*b, limit=limit)
        result += r * b[0]

    return result

def do_simulationp2(filename, limit) -> int:
    blueprints = read_data(filename)
    result = 1

    for b in blueprints[:3]:
        r = simul(*b, limit=limit)
        result *= r

    return result

def test_minerals_p1_example():
    assert do_simulationp1("example.txt", limit=24) == 33

def test_minerals_p1_data():
    assert do_simulationp1("data.txt", limit=24) == 1144

@pytest.mark.skip(reason="P2 took too long time")
def test_minerals_p2_example():
    assert do_simulationp2("example.txt", limit=32) == 3472

@pytest.mark.skip(reason="P2 took too long time")
def test_minerals_p2_data():
    assert do_simulationp2("data.txt", limit=32) == 19980
