def read_data(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


CHARS = "=-012"
CHARS_O = "012=-"


def encode_snafu(result: int) -> str:
    output = ""
    while result:
        result, pos = divmod(result, 5)
        output += CHARS_O[pos]
        if pos > 2:
            result += 1

    return output[::-1]


def sum_snafu(filename: str) -> str:
    data = read_data(filename)

    # Decode & sum
    decoded = [sum([(CHARS.find(n) - 2) * (5 ** i) for i, n in enumerate(line[::-1])])
               for line in data]
    result = sum(decoded)

    # Encode result
    output = encode_snafu(result)
    print(f"{result=} {output=}")
    return output


if __name__ == "__main__":
    assert sum_snafu("example.txt") == "2=-1=0"
    assert sum_snafu("data.txt") == "2-1-110-=01-1-0-0==2"
