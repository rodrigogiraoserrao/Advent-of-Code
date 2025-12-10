from collections import deque

import numpy as np
from scipy.optimize import LinearConstraint, milp


def parse_input_p1(filepath):
    machines = []
    with open(filepath, "r") as f:
        for line in f:
            target, *switches, _ = line.split()
            target = tuple(char == "#" for char in target[1:-1])
            switches = [
                tuple(map(int, switch[1:-1].split(",")))
                for switch in switches
            ]
            machines.append((target, switches))

    return machines


def part1(machines):
    total = 0

    for target, switches in machines:
        start = (False,) * len(target)
        visited = {start}
        queued = deque([(start, 0)])  # FIFO – first in, first out
        while queued:
            state, steps = queued.popleft()
            if state == target:
                total += steps
                break

            for switch in switches:
                new_state = tuple(
                    (not s) if idx in switch else (s)
                    for idx, s in enumerate(state)
                )
                if new_state not in visited:
                    queued.append((new_state, steps + 1))
                    visited.add(new_state)
        else:
            print(visited)

    return total


def parse_input_p2(filepath):
    machines = []
    with open(filepath, "r") as f:
        for line in f:
            _, *switches, target = line.split()
            target = tuple(map(int, target[1:-1].split(",")))
            switches = [
                tuple(map(int, switch[1:-1].split(",")))
                for switch in switches
            ]
            machines.append((target, switches))

    return machines


def part2(machines):
    total = 0

    for target, switches in machines:
        c = np.ones(len(switches), dtype=int)
        b = np.array(target, dtype=int)
        nrows = len(target)
        ncols = len(switches)
        A = np.zeros((nrows, ncols), dtype=int)
        for idx, switch in enumerate(switches):
            for switch_idx in switch:
                A[switch_idx, idx] = 1
        constraints = LinearConstraint(A, b, b)
        integrality = np.ones_like(c)
        res = milp(
            c=c,
            constraints=constraints,
            integrality=integrality,
        )
        total += sum(res.x)

    return total


if __name__ == "__main__":
    machines = parse_input_p1("input.txt")
    print(part1(machines))
    machines = parse_input_p2("input.txt")
    print(part2(machines))