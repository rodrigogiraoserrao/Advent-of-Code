"""🎄 Solution for Day 8 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 08.py
"""

from itertools import combinations, islice
from math import prod

inp = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
part1_asserts = [
    (inp, 40),
]
part2_asserts = [
    (inp, 25272),
]


def part1(inp: str) -> str | int | None:
    points = [
        (idx, tuple(map(int, line.split(","))))
        for idx, line in enumerate(inp.splitlines())
    ]

    max_connections = 10 if len(points) < 25 else 1000

    id_to_circuit = {idx: idx for idx in range(len(points))}
    circuit_to_ids = {idx: {idx} for idx in range(len(points))}

    distances = []
    for (a, (ax, ay, az)), (b, (bx, by, bz)) in combinations(points, 2):
        dist = (ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2
        distances.append((dist, a, b))

    distances.sort(reverse=True)

    for _ in range(max_connections):
        print("-----" * 5 + "\n")
        _, pa, pb = distances.pop()
        if (new_id := id_to_circuit[pa]) == (old_id := id_to_circuit[pb]):
            print(f"Skipping {points[pa]} and {points[pb]}.")
            continue

        print(f"Connecting {points[pa]} and {points[pb]}.")
        for circuit_box in circuit_to_ids[old_id]:
            id_to_circuit[circuit_box] = new_id
        circuit_to_ids[new_id].update(circuit_to_ids[old_id])
        circuit_to_ids[old_id] = set()
        print(circuit_to_ids[new_id])

    # Find the three largest circuits.
    return prod(islice(
        sorted(map(len, circuit_to_ids.values()), reverse=True),
        3,
    ))


def part2(inp: str) -> str | int | None:
    points = [
        (idx, tuple(map(int, line.split(","))))
        for idx, line in enumerate(inp.splitlines())
    ]

    circuits = len(points)

    id_to_circuit = {idx: idx for idx in range(len(points))}
    circuit_to_ids = {idx: {idx} for idx in range(len(points))}

    distances = []
    for (a, (ax, ay, az)), (b, (bx, by, bz)) in combinations(points, 2):
        dist = (ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2
        distances.append((dist, a, b))

    distances.sort(reverse=True)

    while circuits > 1:
        print("-----" * 5 + "\n")
        _, pa, pb = distances.pop()
        if (new_id := id_to_circuit[pa]) == (old_id := id_to_circuit[pb]):
            print(f"Skipping {points[pa]} and {points[pb]}.")
            continue

        print(f"Connecting {points[pa]} and {points[pb]}.")
        circuits -= 1
        if circuits == 1:
            return points[pa][1][0] * points[pb][1][0]

        for circuit_box in circuit_to_ids[old_id]:
            id_to_circuit[circuit_box] = new_id
        circuit_to_ids[new_id].update(circuit_to_ids[old_id])
        circuit_to_ids[old_id] = set()
        print(circuit_to_ids[new_id])

