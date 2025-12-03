"""🎄 Solution for Day 2 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 02.py
"""

inp = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
part1_asserts = [
    (inp, 1227775554),
]
part2_asserts = [
    (inp, 4174379265),
]


def parse_input(inp):
    ranges = [
        tuple(map(int, range_.split("-")))
        for range_ in inp.strip().split(",")
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


def part1(inp):
    """Sums all invalid IDs within the given ranges."""
    ranges = normalise_ranges(parse_input(inp))

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


def part2(inp):
    """Sums all invalid IDs within the given ranges.
    
    Now, an ID is invalid if it is made up of a subpattern of any length.
    """
    ranges = normalise_ranges(parse_input(inp))

    invalid_ids = set()
    for left, right in ranges:
        for left_split, right_split in zip(splits(left), splits(right)):
            for subpattern in range(left_split, right_split + 1):
                multiplier = len(str(left)) // len(str(left_split))
                n = int(multiplier * str(subpattern))
                if left <= n <= right:
                    invalid_ids.add(n)

    return sum(invalid_ids)
