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
        at_signs = {
            (x, y)
            for y, line in enumerate(f) for x, cell in enumerate(line)
            if cell == "@"
        }
    return at_signs


def part1(at_signs):
    final_count = 0
    for x, y in at_signs:
        neighbours = 0
        for dx, dy in _NEIGHBOUR_OFFSETS:
            nx, ny = x + dx, y + dy
            if (nx, ny) in at_signs:
                neighbours += 1
        if neighbours <= 3:
            final_count += 1

    return final_count


def part2(at_signs):
    may_be_removed = at_signs

    was_removed = set()
    while may_be_removed:

        to_be_removed = set()
        next_layer = set()
        for x, y in may_be_removed:
            neighbours = {
                (nx, ny)
                for dx, dy in _NEIGHBOUR_OFFSETS
                if (nx, ny) in at_signs
            }
            if len(neighbours) <= 3:
                to_be_removed.add((x, y))
                next_layer.update(neighbours)

        at_signs -= to_be_removed
        was_removed |= to_be_removed  # was_removed = was_removed | to_be_removed
        may_be_removed = next_layer & at_signs

    return len(was_removed)


if __name__ == "__main__":
    at_signs = parse_input("input.txt")
    print(part1(at_signs))
    print(part2(at_signs))