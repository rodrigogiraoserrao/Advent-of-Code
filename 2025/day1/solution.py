# Solving AoC day 1.
# Given a circular dial and a number of instructions,
# figure out how many times the dial stops at 0.

# Take your input and parse it.
# Simulate a turn of the dial based on a number.
# Make sure the dial works as a circular dial.
# (The dial has 100 positions.)
# 10 -> L20 -> 90


# --- Input parsing.
# Each rotation will be a positive number (if it's a Right)
# or a negative number (if it's a Left).
rotations = []
with open("input.txt", "r") as f:
    for line in f:
        # Distinguish Left and Right rotations.
        direction = line[0]  # 'L' or 'R'
        magnitude = line[1:]  # the number of ticks

        rotations.append(
            (-1 if direction == "L" else 1)
            * int(magnitude)
        )
        """
        if direction == "L":
            rotations.append(-int(magnitude))
        else:
            rotations.append(int(magnitude))
        """

print(rotations[:10])


# --- Part 1.
# Count how many times the dial stops at 0 after a turn.

count = 0
position = 50  # Initial position
for rotation in rotations:
    position += rotation
    position %= 100  # position = position % 100
    if position == 0:
        count += 1

print(count)


# --- Part 2

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

print(count)