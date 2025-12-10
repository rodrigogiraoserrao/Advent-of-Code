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

from collections import deque
import heapq

import numpy as np
from scipy.optimize import LinearConstraint, milp


def apply_light_button(state, wire):
    return tuple(not s if idx in wire else s for idx, s in enumerate(state))


def part1(inp: str) -> str | int | None:
    machines = []
    for line in inp.splitlines():
        state, *wires, _ = line.split()
        state = tuple(char == "#" for char in state[1:-1])
        wires = [tuple(map(int, wire[1:-1].split(","))) for wire in wires]
        machines.append((state, wires))

    total = 0
    for target, wires in machines:
        start = (False,) * len(target)
        queued = deque([(start, 0)])
        visited = {start}
        while queued:
            state, dist = queued.popleft()
            if state == target:
                total += dist
                break
            for wire in wires:
                new_state = apply_light_button(state, wire)
                if new_state not in visited:
                    queued.append((new_state, dist + 1))
                    visited.add(new_state)

    return total


def apply_joltage_wire(joltage, wire):
    return tuple(j - (idx in wire) for idx, j in enumerate(joltage))


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


def _part2(inp: str) -> str | int | None:
    machines = []
    for line in inp.splitlines():
        _, *wires, joltage = line.split()
        joltage = tuple(map(int, joltage[1:-1].split(",")))
        # Convert (2, 4) into (0, 1, 0, 1).
        _wires = []
        for wire in wires:
            nums = set(map(int, wire[1:-1].split(",")))
            _wires.append(tuple(int(idx in nums) for idx in range(len(joltage))))
        wires = _wires
        machines.append((joltage, wires))

    total = 0
    for start, wires in machines if len(machines) < 100 else machines[5:]:
        best_wire = max(sum(w) for w in wires)
        tlen = len(start)
        print(tlen, len(wires))
        target = (0,) * tlen
        queued = []
        heapq.heappush(queued, (max(start), 0, start, range(len(wires))))
        best_dists = {start: 0}
        visited = {start}
        while queued:
            _, dist, state, legal_wires = heapq.heappop(queued)
            if state == target:
                total += dist
                break
            for wire_idx in legal_wires:
                wire = wires[wire_idx]
                new_state = []
                for s, w in zip(state, wire):
                    if w > s:
                        break
                    new_state.append(s - w)
                if len(new_state) < tlen:
                    continue
                new_state = tuple(new_state)
                new_dist = dist + 1
                if new_state not in best_dists or new_dist < best_dists[new_state]:
                    heuristic = new_dist + sum(new_state) / best_wire
                    best_dists[new_state] = new_dist
                    new_legal_wires = [
                        wire_idx
                        for wire_idx in legal_wires
                        if all(s >= w for s, w in zip(new_state, wires[wire_idx]))
                    ]
                    heapq.heappush(
                        queued, (heuristic, new_dist, new_state, new_legal_wires)
                    )
                    visited.add(new_state)

    return total
