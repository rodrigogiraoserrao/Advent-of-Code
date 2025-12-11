"""🎄 Solution for Day 10 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 10.py
"""

inp = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
part1_asserts = [
    (inp, 7),
]
part2_asserts = [
    (inp, 33),
]

from functools import reduce
from itertools import combinations
from operator import xor

import numpy as np
from scipy.optimize import LinearConstraint, milp


def groups_of_buttons(buttons):
    for n in range(1, len(buttons) + 1):
        for group in combinations(buttons, n):
            yield list(group)


def part1(inp: str) -> str | int | None:
    machines = []
    for line in inp.splitlines():
        state, *buttons, _ = line.split()
        state = set(idx for idx, char in enumerate(state[1:-1]) if char == "#")
        buttons = [set(map(int, button[1:-1].split(","))) for button in buttons]
        machines.append((state, buttons))

    total = 0
    for target, buttons in machines:
        for group in groups_of_buttons(buttons):
            if reduce(xor, group) == target:
                total += len(group)
                break

    return total


def part2(inp: str) -> str | int | None:
    machines = []
    for line in inp.splitlines():
        _, *wires, joltage = line.split()
        joltage = tuple(map(int, joltage[1:-1].split(",")))
        _wires = []
        for wire in wires:
            _wires.append(tuple(map(int, wire[1:-1].split(","))))
        wires = _wires
        machines.append((joltage, wires))

    total = 0
    for target, wires in machines:
        b = np.array(target)
        c = np.ones(len(wires), dtype=int)
        A = np.zeros([len(target), len(wires)], dtype=int)
        for idx, wire in enumerate(wires):
            for w in wire:
                A[w, idx] = 1
        constraints = LinearConstraint(A, b, b)
        integrality = np.ones_like(c)
        res = milp(c=c, constraints=constraints, integrality=integrality)
        total += sum(round(v) for v in res.x)

    return total
