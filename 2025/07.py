"""🎄 Solution for Day 7 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 07.py
"""

from collections import Counter

inp = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
part1_asserts = [
    (inp, 21),
]
part2_asserts = [
    (inp, 40),
]


def part1(inp: str) -> str | int | None:
    splitters = []
    header, *splitter_rows = inp.splitlines()
    for row in splitter_rows:
        splitter_locations = {idx for idx, cell in enumerate(row) if cell == "^"}
        if splitter_locations:
            splitters.append(splitter_locations)

    beams = {header.find("S")}
    splits = 0
    for row in splitters:
        hits = beams & row
        splits += len(hits)
        misses = beams - row
        new_beams = {hit - 1 for hit in hits} | {hit + 1 for hit in hits}
        beams = misses | new_beams
    return splits


def part2(inp: str) -> str | int | None:
    splitters = []
    header, *splitter_rows = inp.splitlines()
    for row in splitter_rows:
        splitter_locations = {idx for idx, cell in enumerate(row) if cell == "^"}
        if splitter_locations:
            splitters.append(splitter_locations)

    width = len(header)
    beams = Counter()
    beams[header.find("S")] = 1
    for row in splitters:
        new_beams = Counter()
        for hit in beams.keys() & row:
            if hit >= 1:
                new_beams[hit - 1] += beams[hit]
            if hit <= width - 2:
                new_beams[hit + 1] += beams[hit]
        for miss in beams.keys() - row:
            new_beams[miss] += beams[miss]
        beams = new_beams
    return beams.total()
