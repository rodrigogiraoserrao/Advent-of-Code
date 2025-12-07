def parse_input(filepath):
    with open(filepath, "r") as f:
        splitters = [list(line) for line in f.read().splitlines()]

    return splitters


def part2(splitters):
    S_pos = splitters[0].index("S")
    # 1. We fill the bottom with 1s
    for x, _ in enumerate(splitters[-1]):
        splitters[-1][x] = 1

    # 2. Now, we want to fill the rows from the bottom up
    for y in range(len(splitters) - 2, -1, -1):
        # 3. Let's go through the current row.
        row = splitters[y]
        for x, char in enumerate(row):
            if char == "^":
                continue

            # 4. If this is a dot, but there's a splitter UNDER,
            # you need to combine the positions.
            if splitters[y + 1][x] == "^":
                row[x] = splitters[y + 1][x - 1] + splitters[y + 1][x + 1]
            else:
                row[x] = splitters[y + 1][x]

    return splitters[0][S_pos]


if __name__ == "__main__":
    splitters = parse_input("input.txt")
    print(part2(splitters))