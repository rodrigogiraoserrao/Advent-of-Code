def parse_input(filepath):
    with open(filepath, "r") as f:
        ranges = [
            tuple(map(int, range_.split("-")))
            for range_ in f.read().strip().split(",")
        ]
    return ranges


def normalise_ranges(ranges):
    """Takes a list of ranges and builds another list of ranges
    where all ranges have endpoints with the same number of digits.

    E.g., (10, 23) -> (10, 23);
    (753, 10510) -> [(753, 999), (1000, 9999), (10000, 10510)]
    """
    normalised_ranges = []
    for left, right in ranges:
        for length in range(len(str(left)), len(str(right)) + 1):
            sub_left = (
                left
                if length == len(str(left))
                else int("1" + (length - 1) * "0")
            )
            sub_right = right if length == len(str(right)) else int(length * "9")
            normalised_ranges.append((sub_left, sub_right))
    return normalised_ranges


def halve(n):
    """Take a number with an even number of digits;
    return the integer of the first half.
    """
    s = str(n)
    return int(s[:len(s) // 2])


# mathspp.com/drops
def part1(ranges):
    """Sums all invalid IDs within the given ranges."""
    invalid_ids_sum = 0
    for left, right in ranges:
        if len(str(left)) % 2:
            continue
        hl = halve(left)
        hr = halve(right)
        for half in range(hl, hr + 1):
            n = int(f"{half}{half}")
            if left <= n <= right:
                invalid_ids_sum += n
    return invalid_ids_sum


def splits(n):
    """Returns all prefixes of n (as a string) that have a length
    that evenly divides the number of digits of n.

    Examples:
        123456 -> [1, 12, 123]
        12345678 -> [1, 12, 1234]
        123456789 -> [1, 123]
    """
    s = str(n)
    length = len(s)
    prefixes = []
    for target_length in range(1, length // 2 + 1):
        if length % target_length:
            continue
        prefixes.append(int(s[:target_length]))
    return prefixes


def part2(ranges):
    """Sums all invalid IDs within the given ranges.
    
    Now, an ID is invalid if it is made up of a subpattern of any length.
    """
    invalid_ids = set()
    for left, right in ranges:
        for left_split, right_split in zip(splits(left), splits(right)):
            for subpattern in range(left_split, right_split + 1):
                multiplier = len(str(left)) // len(str(left_split))
                n = int(multiplier * str(subpattern))
                if left <= n <= right:
                    invalid_ids.add(n)

    return sum(invalid_ids)


def main():
    ranges = normalise_ranges(parse_input("input.txt"))
    print(part1(ranges))
    print(part2(ranges))

if __name__ == "__main__":
    main()