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
    grid = [list(row) for row in inp.splitlines()]
    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    removed = set()
    while True:
        marked_for_removal = set()
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != "@":
                    continue
                neighbours = sum(
                    grid[y+dy][x+dx] == "@"
                    for dx, dy in _NEIGHBOUR_OFFSETS
                    if 0 <= y + dy < HEIGHT and 0 <= x + dx < WIDTH
                )
                if neighbours <= 3:
                    marked_for_removal.add((x, y))
        if not marked_for_removal:
            break

        for x, y in marked_for_removal:
            grid[y][x] = "."
        removed.update(marked_for_removal)

    return len(removed)
