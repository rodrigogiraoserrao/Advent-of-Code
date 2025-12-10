"""🎄 Solution for Day 9 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 09.py
"""

inp = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
part1_asserts = [
    (inp, 50),
]
part2_asserts = [
    (inp, None),
]


from itertools import combinations


def part1(inp: str) -> str | int | None:
    corners = [tuple(map(int, line.split(","))) for line in inp.splitlines()]
    return max(
        (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for (x1, y1), (x2, y2) in combinations(corners, 2)
    )


def part2(inp: str) -> str | int | None:
    return None
