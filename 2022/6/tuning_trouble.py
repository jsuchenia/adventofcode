def get_data() -> str:
    with open("data.txt") as f:
        return f.read().strip()


def find_marker(data: str, length=4) -> int:
    for i in range(len(data) - length + 1):
        if len(set(data[i:i + length])) == length:
            return i + length
    return -1


if __name__ == "__main__":
    data = get_data()

    assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert find_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    assert find_marker(data) == 1760
    print("Part I", find_marker(data))

    assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", length=14) == 19
    assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", length=14) == 23
    assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", length=14) == 23
    assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", length=14) == 29
    assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", length=14) == 26
    assert find_marker(data, length=14) == 2974
    print("Part II", find_marker(data, length=14))
