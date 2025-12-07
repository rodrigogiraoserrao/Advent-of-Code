from functools import cache


with open("input.txt", "r") as f:
    splitters = [list(line) for line in f.read().splitlines()]


@cache
def count_paths(x, y) -> int:
    if y == len(splitters) - 1:  # Are we at the bottom?
        return 1

    if splitters[y + 1][x] == "^":
        return count_paths(x - 1, y + 1) + count_paths(x + 1, y + 1)
    else:
        return count_paths(x, y + 1)


if __name__ == "__main__":
    print(count_paths(splitters[0].index("S"), 0))