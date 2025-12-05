def parse_input(filepath):
    with open(filepath, "r") as f:
        ranges = []
        # Go through the lines with ranges until I hit
        # an empty line:
        for line in iter(f.readline, "\n"):
            left, right = map(int, line.split("-"))
            ranges.append(range(left, right + 1))

        ids = []
        # At this point, we're only left with the IDs inside the file.
        for line in f:
            ids.append(int(line))

    return ranges, ids


def part_one(ranges, ids):
    count = 0
    for each_id in ids:
        count += any(each_id in range_ for range_ in ranges)
    return count


def part_two(ranges):
    processed_ranges = []

    ranges_to_process = [
        (range_.start, range_.stop - 1)
        for range_ in ranges
    ]
    while ranges_to_process:
        left, right = ranges_to_process.pop()

        for pl, pr in processed_ranges:
            if pl <= left <= pr:
                left = pr + 1
            if pl <= right <= pr:
                right = pl - 1

            # Does the incoming range fully contain the range to be processed?
            if left < pl <= pr < right:
                ranges_to_process.append((pr + 1, right))
                right = pl - 1

            if left > right:
                break
        else:
            # We append the range only if we didn't break from the loop.
            processed_ranges.append((left, right))

    count = 0
    for left, right in processed_ranges:
        count += right - left + 1
    return count


if __name__ == "__main__":
    ranges, ids = parse_input("input.txt")
    print(part_one(ranges, ids))
    print(part_two(ranges))