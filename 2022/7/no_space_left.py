def build_data(file_name: str):
    with open(file_name) as f:
        data = f.read().split('\n')

    root, stack, cwd = {}, None, None

    for line in data:
        if line.startswith("$ ls"):
            continue
        elif line.startswith("$ cd "):
            cd_param = line[5:]
            if cd_param == "/":
                stack = [root]
                cwd = root
            elif cd_param == "..":
                cwd = stack.pop()
            elif cd_param in cwd:
                stack.append(cwd)
                cwd = cwd[cd_param]
        elif line.startswith("dir "):
            dir_name = line[4:]
            if dir_name not in cwd:
                cwd[dir_name] = {}
        else:
            size, f = line.split(" ")
            cwd[f] = int(size)
    return root


def count_size(name: str, element, dir_sizes: list) -> int:
    if isinstance(element, int):
        return element

    size = sum([count_size(f"{name}/{key}", value, dir_sizes) for key, value in element.items()])

    print(f"dif {name} with size {size}")
    dir_sizes.append((name, size))
    return size


MAX_LIMIT = 40_000_000


def traverse(file_name: str, size_limit: int = 100_000):
    root_dir = build_data(file_name)
    dir_sizes = []
    root_size = count_size("", root_dir, dir_sizes)

    small_sizes = sum([size for name, size in dir_sizes if size <= size_limit])
    print(f"Total weight of small dirs is {small_sizes}")

    found = [size for name, size in dir_sizes if size >= root_size - MAX_LIMIT]
    found.sort()
    print(f"Smallest one that fit is {found[0]}")

    result = (small_sizes, found[0])
    print(f"{result=}")
    return result


if __name__ == "__main__":
    assert traverse("example.txt") == (95437, 24933642)
    assert traverse("data.txt") == (1581595, 1544176)
