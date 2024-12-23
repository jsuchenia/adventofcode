# LAN Party - https://adventofcode.com/2024/day/23
from itertools import combinations

from networkx import Graph, find_cliques, enumerate_all_cliques


def get_data(filename: str) -> Graph:
    with open(filename) as f:
        edges = [line.split("-") for line in f.read().strip().splitlines()]
        return Graph(incoming_graph_data=edges)


def q1(filename: str) -> int:
    data = get_data(filename)
    result = 0
    
    # plt.figure(1, figsize=(1920 / 100, 1080 / 100), dpi=100)
    # draw(data, with_labels=False, node_size=500)
    # plt.savefig(f"visualization-{filename}.png")

    for clique in enumerate_all_cliques(data):
        if len(clique) == 3 and any(node.startswith("t") for node in clique):
            result += 1
    return result


def all_subcombinations(connections: set[str]) -> list[str]:
    for i in range(4, len(connections) + 1):
        for combination in combinations(connections, i):
            yield ','.join(sorted(combination))


def q2(filename: str) -> str:
    data = get_data(filename)

    # strongly_connected = defaultdict(int)
    # for node in data.nodes:
    #     for combination in all_subcombinations(set(data.neighbors(node)) | {node}):
    #         strongly_connected[combination] += 1
    #
    # longest_valid = None
    # for combination, count in strongly_connected.items():
    #     if combination.count(',') + 1 == count:
    #         if longest_valid is None or len(combination) > len(longest_valid):
    #             longest_valid = combination
    # return longest_valid

    longest_clique = sorted(find_cliques(data), key=len, reverse=True)[0]
    return ','.join(sorted(longest_clique))


def test_q1():
    assert q1("test.txt") == 7
    assert q1("data.txt") == 998


def test_q2():
    assert q2("test.txt") == "co,de,ka,ta"
    assert q2("data.txt") == "cc,ff,fh,fr,ny,oa,pl,rg,uj,wd,xn,xs,zw"
