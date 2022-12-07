def build_data(file_name: str):
    with open(file_name) as f:
        data = f.read().split('\n')

    root_dir = {}
    stack = None
    curr_dir = None

    for line in data:
        if line.startswith("$ "):
            if line.startswith("$ cd "):
                new_dir = line[5:]
                if new_dir == "/":
                    stack = [root_dir]
                    curr_dir = root_dir
                elif new_dir == "..":
                    curr_dir = stack.pop()
                elif new_dir in curr_dir:
                    stack.append(curr_dir)
                    curr_dir = curr_dir[new_dir]
                else:
                    raise Exception("Unknown directory " + new_dir)
        else:
            if line.startswith("dir "):
                dir_name = line[4:]
                if dir_name not in curr_dir:
                    curr_dir[dir_name] = {}
                else:
                    raise Exception("Diplicated directory " + dir_name)
            else:
                size, f = line.split(" ")
                curr_dir[f] = int(size)
    return root_dir


def count_size(dir_name: str, dir: dict) -> (int, list):
    size = 0
    bigdirs = []

    for name, value in dir.items():
        if isinstance(value, dict):
            new_name = dir_name + "/" + name
            dir_size, dirs = count_size(new_name, value)
            bigdirs += dirs
            bigdirs.append((new_name, dir_size))
            size += dir_size
            print(f"dif {new_name} with size {size}")
        elif isinstance(value, int):
            size += value
        else:
            raise Exception(f"Wrong entry in dirmap {name} {value}")
    return size, bigdirs


MAX_LIMIT = 40000000


def traverse(file_name: str, size_limit: int = 100000):
    root_dir = build_data(file_name)
    root_size, dir_sizes = count_size("", root_dir)

    small_sizes = sum([size for name, size in dir_sizes if size <= size_limit])
    print(small_sizes)

    to_delete = root_size - MAX_LIMIT

    choosen = [size for name, size in dir_sizes if size >= to_delete]
    choosen.sort()
    print(f"Smallest one that fit {to_delete} is {choosen[0]}")

    return small_sizes, choosen[0]


if __name__ == "__main__":
    assert traverse("example.txt") == (95437, 24933642)
    assert traverse("data.txt") == (1581595, 1544176)
