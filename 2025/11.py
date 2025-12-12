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

from collections import defaultdict
from itertools import pairwise
import math


def part1(inp: str) -> str | int | None:
    connections = {}
    for line in inp.splitlines():
        from_, _, to_ = line.partition(": ")
        connections[from_] = to_.split()

    def traverse(from_, to_):
        if from_ == to_:
            return 1

        return sum(traverse(neighb, to_) for neighb in connections[from_])

    return traverse("you", "out")


def build_sources_mapping(connections: dict[str, set[str]]) -> dict[str, set[str]]:
    """Build a reverse mapping from neighbours to origin vertices."""
    rev_connections: dict[str, set[str]] = defaultdict(set)
    for from_, to_ in connections.items():
        for t in to_:
            rev_connections[t].add(from_)

    return rev_connections


def compute_reachable(start: str, connections: dict[str, set[str]]) -> set[str]:
    """Find all reachable vertices from the given starting point."""

    queued: set[str] = {start}
    reachable: set[str] = {start}
    while queued:
        this = queued.pop()
        new_reachable = connections[this] - reachable
        queued.update(new_reachable)
        reachable.update(new_reachable)

    return reachable


def count_paths(
    from_: str,
    to_: str,
    connections: dict[str, set[str]],
    admissible: set[str],
) -> int:
    """Count the paths between the two endpoints that only use admissible points."""
    if from_ == to_:
        return 1

    return sum(
        count_paths(neighb, to_, connections, admissible)
        for neighb in connections[from_] & admissible
    )


def part2(inp: str) -> str | int | None:
    connections = {}
    for line in inp.splitlines():
        from_, _, to_ = line.partition(": ")
        connections[from_] = set(to_.split())
    connections["out"] = set()
    rev_connections = build_sources_mapping(connections)

    go_through: set[str] = {"fft", "dac"}
    reachable: dict[str, set[str]] = {
        from_: compute_reachable(from_, connections) for from_ in go_through
    }
    counts: dict[str, int] = {
        from_: sum(from_ in reachable[other] for other in go_through if other != from_)
        for from_ in go_through
    }
    ordered_go_through: list[str] = sorted(counts.keys(), key=counts.get)
    ordered_go_through = ["svr"] + ordered_go_through + ["out"]

    segments: list[int] = []
    for from_, to_ in pairwise(ordered_go_through):
        admissible = compute_reachable(to_, rev_connections)
        segments.append(count_paths(from_, to_, connections, admissible))

    print(segments)
    return math.prod(segments)
