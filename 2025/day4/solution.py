_NEIGHBOUR_OFFSETS = (
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
)


def parse_input(filepath):
    with open(filepath, "r") as f:
        grid = [
            list(line.strip())
            for line in f
        ]
    return grid


def part1(grid):
    height = len(grid)
    width = len(grid[0])

    final_count = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != "@":
                continue

            neighbours = 0
            for dx, dy in _NEIGHBOUR_OFFSETS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == "@":
                    neighbours += 1
            if neighbours <= 3:
                final_count += 1

    return final_count


def part2(grid):
    height = len(grid)
    width = len(grid[0])

    final_count = 0
    while True:
        to_be_removed = []
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != "@":
                    continue

                neighbours = 0
                for dx, dy in _NEIGHBOUR_OFFSETS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == "@":
                        neighbours += 1
                if neighbours <= 3:
                    to_be_removed.append((x, y))

        if not to_be_removed:
            break

        for x, y in to_be_removed:
            grid[y][x] = "."
        final_count += len(to_be_removed)

    return final_count


if __name__ == "__main__":
    grid = parse_input("input.txt")
    print(part1(grid))
    print(part2(grid))