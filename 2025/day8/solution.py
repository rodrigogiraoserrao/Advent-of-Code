from dataclasses import dataclass, field
from math import prod
from itertools import combinations, count, islice


_POINT_COUNTER = count()


@dataclass
class Point:
    x: int
    y: int
    z: int
    id_: int = field(init=False)

    def __post_init__(self):
        self.id_ = next(_POINT_COUNTER)


def parse_input(filepath):
    with open(filepath, "r") as f:
        # Each point is a pair (id, coordinates).
        points = [
            Point(*map(int, line.split(",")))
            for line in f
        ]
    return points


def compute_paired_distances(points):
    distances = []
    for pa, pb in combinations(points, 2):
        dist = (pa.x - pb.x) ** 2 + (pa.y - pb.y) ** 2 + (pa.z - pb.z) ** 2
        distances.append((dist, pa, pb))
    distances.sort()
    return distances


def part1(points, distances, connections):
    point_to_circuit_id = [p.id_ for p in points]
    circuits = {
        p.id_: {p.id_}
        for p in points
    }

    for idx in range(connections):
        _, pa, pb = distances[idx]
        a_circuit_id = point_to_circuit_id[pa.id_]
        b_circuit_id = point_to_circuit_id[pb.id_]
        if a_circuit_id == b_circuit_id:
            continue

        full_circuit = circuits[a_circuit_id] | circuits[b_circuit_id]

        for point_id in circuits[b_circuit_id]:
            point_to_circuit_id[point_id] = a_circuit_id
        
        circuits[a_circuit_id] = full_circuit
        del circuits[b_circuit_id]

    circuit_sizes = map(len, circuits.values())
    return prod(
        islice(sorted(circuit_sizes, reverse=True), 3)
    )


def part2(points, distances):
    point_to_circuit_id = [p.id_ for p in points]
    circuits = {
        p.id_: {p.id_}
        for p in points
    }

    for _, pa, pb in distances:
        a_circuit_id = point_to_circuit_id[pa.id_]
        b_circuit_id = point_to_circuit_id[pb.id_]

        if a_circuit_id == b_circuit_id:
            continue

        full_circuit = circuits[a_circuit_id] | circuits[b_circuit_id]

        for point_id in circuits[b_circuit_id]:
            point_to_circuit_id[point_id] = a_circuit_id
        
        circuits[a_circuit_id] = full_circuit
        del circuits[b_circuit_id]

        if len(circuits) == 1:
            break

    return pa.x * pb.x


if __name__ == "__main__":
    points = parse_input("input.txt")
    distances = compute_paired_distances(points)
    print(part1(points, distances, 1000))
    print(part2(points, distances))