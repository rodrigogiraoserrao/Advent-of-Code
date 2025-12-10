from functools import reduce
from itertools import combinations
from operator import xor


def parse_input(filepath):
    machines = []
    with open(filepath, "r") as f:
        for line in f:
            target, *switches, _ = line.split()
            target = {idx for idx, char in enumerate(target) if char == "#"}
            switches = [
                set(map(int, switch[1:-1].split(",")))
                for switch in switches
            ]
            machines.append((target, switches))

    return machines


def part1(machines):
    total = 0

    for target, switches in machines:
        done = False
        for n in range(1, len(switches) + 1):
            for used_switches in combinations(switches, n):
                state = reduce(xor, used_switches)
                if state == target:
                    total += n
                    done = True
                    break
            if done:
                break

    return total


if __name__ == "__main__":
    machines = parse_input("input.txt")
    print(part1(machines))