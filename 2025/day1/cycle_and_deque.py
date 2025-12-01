"""
Solving parts 1 and 2 with `deque`.
"""

# from itertools import cycle
from collections import deque

# A deque allows popping and appending (like a list)
# from both ends, efficiently.
# (A list only pops/appends efficiently on the right.)

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


# --- Part 1
dial = deque(range(100))
dial.rotate(50)  # Initial position.

count = 0
for rotation in rotations:
    dial.rotate(rotation)
    if dial[0] == 0:
        count += 1
print(count)


# --- Part 2
dial = deque(range(100))
dial.rotate(50)  # Initial position.

count = 0
for rotation in rotations:
    tick = -1 if rotation < 0 else +1
    for _ in range(abs(rotation)):
        dial.rotate(tick)
        if dial[0] == 0:
            count += 1
print(count)