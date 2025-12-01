def parse_input():
    rots = []

    with open("input.txt", "r") as f:
        for line in f:
            direction, magnitude = line[0], line[1:]
            rots.append(
                (1 if direction == "R" else -1)
                * int(magnitude)
            )
    return rots

rots = parse_input()

# --- Part 1
count = 0
pos = 50
for rot in rots:
    pos += rot
    pos %= 100
    if pos == 0:
        count += 1
print(count)

# --- Part 2
count = 0
pos = 50
for rot in rots:
    full_turns = int(rot / 100)
    count += abs(full_turns)
    rot -= 100 * full_turns

    if not rot:
        continue

    new_pos = pos + rot
    if pos > 0 and new_pos <= 0 or new_pos >= 100:
        count += 1
    pos = new_pos % 100
print(count)
