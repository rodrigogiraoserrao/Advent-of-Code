"""🎄 Solution for Day 11 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 11.py
"""

inp = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

inp2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""
part1_asserts = [
    (inp, 5),
]
part2_asserts = [
    (inp2, 2),
]

from functools import cache


def part1(inp: str) -> str | int | None:
    connections = {}
    for line in inp.splitlines():
        start, _, targets = line.partition(": ")
        connections[start] = targets.split()

    def count_paths(start, target):
        if start == target:
            return 1

        return sum(count_paths(neighb, target) for neighb in connections[start])

    return count_paths("you", "out")


def part2(inp: str) -> str | int | None:
    connections = {}
    for line in inp.splitlines():
        from_, _, to_ = line.partition(": ")
        connections[from_] = to_.split()

    @cache
    def traverse(from_, to_, dac=False, fft=False):
        if from_ == to_:
            return dac == fft == True

        return sum(
            traverse(neighb, to_, dac or neighb == "dac", fft or neighb == "fft")
            for neighb in connections[from_]
        )

    return traverse("svr", "out")
