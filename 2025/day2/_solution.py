def read_ranges(filepath):
    """Read ranges as pairs of strings."""
    with open(filepath, "r") as f:
        ranges = [
            range_.split("-")
            for range_ in f.read().strip().split(",")
        ]

    return ranges


def normalise_ranges(ranges):
    """Normalise ranges from pairs of strings into pairs of integers of the same magnitude.

    E.g., ('10', '20') becomes (10, 20) but ('10', '113') becomes [(10, 99), (100, 113)].
    """
    normalised_ranges = []
    for left, right in ranges:
        for length in range(len(left), len(right) + 1):
            sub_left = left if length == len(left) else "1" + (length - 1) * "0"
            sub_right = right if length == len(right) else length * "9"
            normalised_ranges.append((int(sub_left), int(sub_right)))
    return normalised_ranges


def halve(n):
    """Returns the first half of the characters from the given integer as a string.

    E.g., 1234 -> 12.
    """
    s = str(n)
    return int(s[:len(s) // 2])


def part1(ranges):
    """Sums the invalid IDs in the given normalised ranges.

    An invalid ID is any ID that's made up of the same substring twice.
    E.g., 1212 or 378378.
    """
    invalid_ids_sum = 0
    for left, right in ranges:
        if len(str(left)) % 2:  # Odd length, can't be split in half.
            continue
        hl = halve(left)
        hr = halve(right)
        for half in range(hl, hr + 1):
            n = int(str(half) + str(half))
            if left <= n <= right:
                invalid_ids_sum += n
    return invalid_ids_sum


def splits(n):
    """Returns the prefixes of str(n) with a length that divides the length of str(n).

    E.g., 1234 -> [1, 12]; 123456 -> [1, 12, 123]; 12345678 -> [1, 12, 1234].
    """
    s = str(n)
    l = len(s)
    prefixes = []
    for length in range(1, len(s) // 2 + 1):
        if l % length:
            continue
        prefixes.append(int(s[:length]))
    return prefixes


def part2(ranges):
    """Sums the invalid IDs in the given normalised ranges.

    An invalid ID is any ID that's made up of a repeated substring.
    E.g., 1212 or 373737.
    """
    invalid_ids = set()
    for left, right in ranges:
        for subl, subr in zip(splits(left), splits(right)):
            multiplier = len(str(left)) // len(str(subl))
            for sub in range(subl, subr + 1):
                n = int(multiplier * str(sub))
                if left <= n <= right:
                    invalid_ids.add(n)
    return sum(invalid_ids)


def main():
    ranges = read_ranges("input.txt")
    normalised_ranges = normalise_ranges(ranges)
    print(part1(normalised_ranges))
    print(part2(normalised_ranges))


if __name__ == "__main__":
    main()
