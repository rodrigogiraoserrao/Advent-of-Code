import re

HALF = re.compile(r"^(\d+)\1$")
REPEATED = re.compile(r"^(\d+)\1+$")

def read_ranges(filepath):
    """Read ranges as pairs of integers."""
    with open(filepath, "r") as f:
        ranges = [
            tuple(map(int, range_.split("-")))
            for range_ in f.read().strip().split(",")
        ]

    return ranges


def part1(ranges):
    """Sums the invalid IDs in the given ranges.

    An invalid ID is any ID that's made up of the same substring twice.
    E.g., 1212 or 378378.
    """
    invalid_ids_sum = 0
    for left, right in ranges:
        for number in range(left, right + 1):
            if HALF.match(str(number)):
                invalid_ids_sum += number
    return invalid_ids_sum


def part2(ranges):
    """Sums the invalid IDs in the given normalised ranges.

    An invalid ID is any ID that's made up of a repeated substring.
    E.g., 1212 or 373737.
    """
    invalid_ids_sum = 0
    for left, right in ranges:
        for number in range(left, right + 1):
            if REPEATED.match(str(number)):
                invalid_ids_sum += number
    return invalid_ids_sum


def main():
    ranges = read_ranges("input.txt")
    print(part1(ranges))
    print(part2(ranges))


if __name__ == "__main__":
    main()
