import bisect

def parse_input(filepath):
    with open(filepath, "r") as f:
        ranges = []
        # Go through the lines with ranges until I hit
        # an empty line:
        for line in iter(f.readline, "\n"):
            left, right = map(int, line.split("-"))
            ranges.append((left, right))

        ids = []
        # At this point, we're only left with the IDs inside the file.
        for line in f:
            ids.append(int(line))

    return ranges, ids


def normalise_ranges(ranges):
    ticks = []
    for left, right in ranges:
        ticks.append((left, +1))
        ticks.append((right, -1))

    # Make sure we sort in ascending order by tick position
    # and in DEScending order by depth delta so that
    # starting ticks show up before ending ticks.
    ticks = sorted(ticks, key=lambda t: (t[0], -t[1]))
    normalised_ranges = []
    depth = 0
    left = None
    for pos, delta_depth in ticks:
        depth += delta_depth
        assert depth >= 0
        if delta_depth == 1 and depth == 1:
            left = pos
        elif depth == 0:
            normalised_ranges.append((left, pos))
            left = None

    return normalised_ranges


def part2(ranges):
    count = 0
    for left, right in ranges:
        count += right - left + 1
    return count


def part1(normalised_ranges, ids):
    count = 0
    lefts = [left for left, _ in normalised_ranges]
    for id_ in ids:
        idx = bisect.bisect_right(lefts, id_) - 1
        if idx >= 0:
            count += id_ <= normalised_ranges[idx][1]

    return count


if __name__ == "__main__":
    ranges, ids = parse_input("input.txt")
    ranges = normalise_ranges(ranges)
    print(part1(ranges, ids))
    print(part2(ranges))