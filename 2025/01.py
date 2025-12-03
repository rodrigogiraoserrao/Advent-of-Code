"""🎄 Solution for Day 1 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 01.py
"""

inp = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

part1_asserts = [
    (inp, 3)
]

part2_asserts = [
    (inp, 6)
]

# Each rotation will be a positive number (if it's a Right)
# or a negative number (if it's a Left).
def parse_input(inp):
    rotations = []
    for line in inp.splitlines():
        # Distinguish Left and Right rotations.
        direction = line[0]  # 'L' or 'R'
        magnitude = line[1:]  # the number of ticks

        rotations.append(
            (-1 if direction == "L" else 1)
            * int(magnitude)
        )
    return rotations


def part1(inp):
    rotations = parse_input(inp)
    count = 0
    position = 50  # Initial position
    for rotation in rotations:
        position += rotation
        position %= 100  # position = position % 100
        if position == 0:
            count += 1
    return count


def part2(inp):
    rotations = parse_input(inp)
    count = 0
    position = 50
    for rotation in rotations:
        full_turns = int(rotation / 100)
        count += abs(full_turns)
        rotation -= 100 * full_turns  # What's left after the full turns.

        # Either you were close to 0 and `rotation` is negative
        # and now `new_position` is negative
        # OR `position` was close to 99, `rotation` is positive
        # and now `new_position` is greater than 100.
        new_position = position + rotation
        if (
            (position > 0 and new_position <= 0)
            or (new_position >= 100)
        ):
            count += 1
        position = new_position % 100

    return count
