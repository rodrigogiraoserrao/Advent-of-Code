"""Solving PART 1 ONLY with `itertools.accumulate`."""

from itertools import accumulate

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


def turn_dial(position, turn):
    """Return the new dial position after the given turn."""
    return (position + turn) % 100

all_dial_positions = accumulate(
    rotations,
    # accumulate needs a function that
    # takes 2 arguments and returns
    # a result.
    # The left argument is the
    # previous partial result.
    # The right argument is the
    # new value you're processing.
    # The return value is the
    # current partial result.
    turn_dial,
    initial=50,
)

count = 0
for position in all_dial_positions:
    if position == 0:
        count += 1

print(count)