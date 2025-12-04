"""🎄 Solution for Day 4 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 04.py
"""

inp = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
part1_asserts = [
    (inp, 13),
]
part2_asserts = [
    (inp, 43),
]


_NEIGHBOUR_OFFSETS = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))


def part1(inp: str) -> str | int | None:
    grid = inp.splitlines()
    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    count = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != "@":
                continue
            neighbours = sum(
                grid[y+dy][x+dx] == "@"
                for dx, dy in _NEIGHBOUR_OFFSETS
                if 0 <= y + dy < HEIGHT and 0 <= x + dx < WIDTH
            )
            count += neighbours <= 3
    return count


def part2(inp: str) -> str | int | None:
    rolls = {
        (x, y)
        for y, row in enumerate(inp.splitlines())
        for x, cell in enumerate(row)
        if cell == "@"
    }

    removed = set()
    may_be_removed = rolls
    while True:
        marked_for_removal = set()
        neighbours_of_removals = set()
        for x, y in may_be_removed:
            neighbours = {
                (x + dx, y + dy)
                for dx, dy in _NEIGHBOUR_OFFSETS
                if (x + dx, y + dy) in rolls
            }
            if len(neighbours) <= 3:
                marked_for_removal.add((x, y))
                neighbours_of_removals.update(neighbours)

        if not marked_for_removal:
            break

        rolls -= marked_for_removal
        removed |= marked_for_removal
        may_be_removed = neighbours_of_removals

    return len(removed)
